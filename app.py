import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename

from config import GEMINI_API_KEY
from utils.summary_helper import generate_analysis_summary
from services.resume_parser_service import parse_resume
from services.history_service import (
    save_analysis,
    get_user_history,
    update_generated_questions,
    delete_selected_history,
    delete_all_history
)
from services.auth_service import register_user, login_user
from services.gemini_question_service import generate_questions_with_gemini
from services.report_service import create_analysis_report
from services.course_service import get_course_recommendations
from agents.ats_agent import calculate_ats_score
from agents.skill_gap_agent import analyze_skill_gap
from agents.feedback_agent import generate_feedback

app = Flask(__name__)
app.secret_key = "agentic_ai_secret_key"

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def prepare_history_data(user_email):
    history_data = get_user_history(user_email)

    for item in history_data:
        item["matched_skills"] = item["matched_skills"].split(", ") if item["matched_skills"] else []
        item["missing_skills"] = item["missing_skills"].split(", ") if item["missing_skills"] else []

        if item.get("generated_questions"):
            item["generated_questions_list"] = item["generated_questions"].split("||")
        else:
            item["generated_questions_list"] = []

    return history_data


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login", methods=["POST"])
def do_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = login_user(email, password)

    if user:
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        return redirect(url_for("dashboard"))

    return render_template("login.html", error="Invalid email or password")


@app.route("/register-user", methods=["POST"])
def do_register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    success = register_user(name, email, password)

    if success:
        return render_template("login.html", success="Registration successful. Please login.")

    return render_template("register.html", error="Email already exists")


@app.route("/dashboard")
def dashboard():
    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", user_name=session["user_name"])


@app.route("/upload")
def upload():
    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template("upload_resume.html")


@app.route("/history")
def history():
    if "user_name" not in session:
        return redirect(url_for("login"))

    history_data = prepare_history_data(session["user_email"])
    return render_template("history.html", history=history_data)


@app.route("/delete-selected-history", methods=["POST"])
def delete_selected():
    if "user_name" not in session:
        return redirect(url_for("login"))

    selected_ids = request.form.getlist("selected_history")
    selected_ids = [int(x) for x in selected_ids if x.isdigit()]

    deleted_count = delete_selected_history(session["user_email"], selected_ids)
    history_data = prepare_history_data(session["user_email"])

    if deleted_count > 0:
        return render_template(
            "history.html",
            history=history_data,
            success=f"{deleted_count} selected history item(s) deleted successfully."
        )

    return render_template(
        "history.html",
        history=history_data,
        error="No history items were selected."
    )


@app.route("/delete-all-history", methods=["POST"])
def delete_all():
    if "user_name" not in session:
        return redirect(url_for("login"))

    deleted_count = delete_all_history(session["user_email"])
    history_data = prepare_history_data(session["user_email"])

    if deleted_count > 0:
        return render_template(
            "history.html",
            history=history_data,
            success="All history deleted successfully."
        )

    return render_template(
        "history.html",
        history=history_data,
        error="No history available to delete."
    )


@app.route("/compare")
def compare():
    if "user_name" not in session:
        return redirect(url_for("login"))

    history_data = prepare_history_data(session["user_email"])
    comparison_data = history_data[:3]

    return render_template("compare.html", comparison_data=comparison_data)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/analyze", methods=["POST"])
def analyze():
    if "user_name" not in session:
        return redirect(url_for("login"))

    role = request.form.get("role")
    career_goal = request.form.get("job_description")
    resume_file = request.files.get("resume")

    if not resume_file or resume_file.filename == "":
        return render_template("upload_resume.html", error="Please upload a resume file.")

    if not allowed_file(resume_file.filename):
        return render_template("upload_resume.html", error="Only PDF and DOCX files are allowed.")

    filename = secure_filename(resume_file.filename)
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    resume_file.save(resume_path)

    parsed_resume = parse_resume(resume_path)

    target_skills, matched_skills, missing_skills, match_percentage = analyze_skill_gap(
        parsed_resume["skills"], career_goal
    )

    ats_score, ats_remarks, ats_breakdown = calculate_ats_score(
        parsed_resume,
        target_skills,
        matched_skills
    )

    suggestions = generate_feedback(missing_skills, ats_remarks)
    course_recommendations = get_course_recommendations(missing_skills)
    analysis_summary = generate_analysis_summary(role, ats_score, missing_skills, match_percentage)

    save_analysis(
        session["user_email"],
        parsed_resume["name"],
        role,
        filename,
        ats_score,
        matched_skills,
        missing_skills,
        career_goal,
        match_percentage,
        ats_breakdown,
        analysis_summary
    )

    return render_template(
        "results.html",
        role=role,
        career_goal=career_goal,
        filename=filename,
        parsed_resume=parsed_resume,
        ats_score=ats_score,
        ats_remarks=ats_remarks,
        ats_breakdown=ats_breakdown,
        target_skills=target_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        matched_count=len(matched_skills),
        missing_count=len(missing_skills),
        match_percentage=match_percentage,
        analysis_summary=analysis_summary,
        suggestions=suggestions,
        course_recommendations=course_recommendations,
        interview_questions=[],
        selected_difficulty="Easy",
        question_count=5,
        question_error=None
    )


@app.route("/generate-questions", methods=["POST"])
def generate_questions():
    if "user_name" not in session:
        return redirect(url_for("login"))

    role = request.form.get("role")
    career_goal = request.form.get("career_goal")
    filename = request.form.get("filename")

    parsed_name = request.form.get("parsed_name")
    parsed_email = request.form.get("parsed_email")
    parsed_phone = request.form.get("parsed_phone")
    parsed_skills_raw = request.form.get("parsed_skills", "")
    target_skills_raw = request.form.get("target_skills", "")
    matched_skills_raw = request.form.get("matched_skills", "")
    missing_skills_raw = request.form.get("missing_skills", "")
    ats_score = int(request.form.get("ats_score"))
    match_percentage = int(request.form.get("match_percentage"))
    difficulty = request.form.get("difficulty")
    question_count = int(request.form.get("question_count"))

    parsed_skills = parsed_skills_raw.split("||") if parsed_skills_raw else []
    target_skills = target_skills_raw.split("||") if target_skills_raw else []
    matched_skills = matched_skills_raw.split("||") if matched_skills_raw else []
    missing_skills = missing_skills_raw.split("||") if missing_skills_raw else []

    parsed_resume = {
        "name": parsed_name,
        "email": parsed_email,
        "phone": parsed_phone,
        "skills": parsed_skills,
        "resume_text": ""
    }

    ats_score, ats_remarks, ats_breakdown = calculate_ats_score(
        parsed_resume,
        target_skills,
        matched_skills
    )

    suggestions = generate_feedback(missing_skills, ats_remarks)
    course_recommendations = get_course_recommendations(missing_skills)
    analysis_summary = generate_analysis_summary(role, ats_score, missing_skills, match_percentage)

    try:
        interview_questions = generate_questions_with_gemini(
            api_key=GEMINI_API_KEY,
            role=role,
            missing_skills=missing_skills,
            difficulty=difficulty,
            question_count=question_count,
            career_goal=career_goal
        )

        update_generated_questions(
            session["user_email"],
            filename,
            role,
            difficulty,
            question_count,
            "||".join(interview_questions)
        )

        error_message = None

    except Exception:
        interview_questions = []
        error_message = "Question generation is temporarily unavailable due to high API demand. Please try again in a few moments."

    return render_template(
        "results.html",
        role=role,
        career_goal=career_goal,
        filename=filename,
        parsed_resume=parsed_resume,
        ats_score=ats_score,
        ats_remarks=ats_remarks,
        ats_breakdown=ats_breakdown,
        target_skills=target_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        matched_count=len(matched_skills),
        missing_count=len(missing_skills),
        match_percentage=match_percentage,
        analysis_summary=analysis_summary,
        suggestions=suggestions,
        course_recommendations=course_recommendations,
        interview_questions=interview_questions,
        selected_difficulty=difficulty,
        question_count=question_count,
        question_error=error_message
    )


@app.route("/download-report", methods=["POST"])
def download_report():
    if "user_name" not in session:
        return redirect(url_for("login"))

    role = request.form.get("role")
    career_goal = request.form.get("career_goal")
    filename = request.form.get("filename")

    parsed_name = request.form.get("parsed_name")
    parsed_email = request.form.get("parsed_email")
    parsed_phone = request.form.get("parsed_phone")
    parsed_skills_raw = request.form.get("parsed_skills", "")
    target_skills_raw = request.form.get("target_skills", "")
    matched_skills_raw = request.form.get("matched_skills", "")
    missing_skills_raw = request.form.get("missing_skills", "")
    ats_remarks_raw = request.form.get("ats_remarks", "")
    interview_questions_raw = request.form.get("interview_questions", "")
    ats_score = int(request.form.get("ats_score"))
    match_percentage = int(request.form.get("match_percentage"))
    analysis_summary = request.form.get("analysis_summary", "")

    contact_score = int(request.form.get("contact_score", 0))
    skills_score = int(request.form.get("skills_score", 0))
    content_quality_score = int(request.form.get("content_quality_score", 0))
    section_presence_score = int(request.form.get("section_presence_score", 0))
    alignment_score = int(request.form.get("alignment_score", 0))
    writing_score = int(request.form.get("writing_score", 0))

    parsed_skills = parsed_skills_raw.split("||") if parsed_skills_raw else []
    target_skills = target_skills_raw.split("||") if target_skills_raw else []
    matched_skills = matched_skills_raw.split("||") if matched_skills_raw else []
    missing_skills = missing_skills_raw.split("||") if missing_skills_raw else []
    ats_remarks = ats_remarks_raw.split("||") if ats_remarks_raw else []
    interview_questions = interview_questions_raw.split("||") if interview_questions_raw else []

    parsed_resume = {
        "name": parsed_name,
        "email": parsed_email,
        "phone": parsed_phone,
        "skills": parsed_skills
    }

    ats_breakdown = {
        "contact_score": contact_score,
        "skills_score": skills_score,
        "content_quality_score": content_quality_score,
        "section_presence_score": section_presence_score,
        "alignment_score": alignment_score,
        "writing_score": writing_score
    }

    suggestions = generate_feedback(missing_skills, ats_remarks)

    report_filename = f"analysis_report_{session['user_name'].replace(' ', '_')}.pdf"
    report_path = os.path.join(app.config["REPORT_FOLDER"], report_filename)

    create_analysis_report(
        output_path=report_path,
        role=role,
        career_goal=career_goal,
        filename=filename,
        parsed_resume=parsed_resume,
        ats_score=ats_score,
        ats_remarks=ats_remarks,
        ats_breakdown=ats_breakdown,
        target_skills=target_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        match_percentage=match_percentage,
        analysis_summary=analysis_summary,
        suggestions=suggestions,
        interview_questions=interview_questions
    )

    return send_file(report_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)