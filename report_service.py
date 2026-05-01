from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

def create_analysis_report(
    output_path,
    role,
    career_goal,
    filename,
    parsed_resume,
    ats_score,
    ats_remarks,
    ats_breakdown,
    target_skills,
    matched_skills,
    missing_skills,
    match_percentage,
    analysis_summary,
    suggestions,
    interview_questions
):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    y = height - 40
    left_margin = 40
    max_width = width - 80

    def write_line(text, font="Helvetica", size=10, gap=16):
        nonlocal y
        c.setFont(font, size)
        c.drawString(left_margin, y, text)
        y -= gap

    def write_wrapped_text(label, text, font="Helvetica", size=10, gap=14):
        nonlocal y
        c.setFont("Helvetica-Bold", size)
        c.drawString(left_margin, y, label)
        y -= gap

        wrapped = simpleSplit(text, font, size, max_width)
        c.setFont(font, size)
        for line in wrapped:
            if y < 60:
                c.showPage()
                y = height - 40
                c.setFont(font, size)
            c.drawString(left_margin, y, line)
            y -= gap
        y -= 6

    def write_list(title, items):
        nonlocal y
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left_margin, y, title)
        y -= 16

        if not items:
            c.setFont("Helvetica", 10)
            c.drawString(left_margin + 12, y, "None")
            y -= 16
        else:
            for item in items:
                wrapped = simpleSplit(f"• {item}", "Helvetica", 10, max_width - 12)
                for line in wrapped:
                    if y < 60:
                        c.showPage()
                        y = height - 40
                    c.setFont("Helvetica", 10)
                    c.drawString(left_margin + 12, y, line)
                    y -= 14
        y -= 6

    c.setFont("Helvetica-Bold", 16)
    c.drawString(left_margin, y, "Resume Analysis Report")
    y -= 24

    write_line(f"Target Role: {role}", "Helvetica-Bold", 11)
    write_line(f"Uploaded Resume: {filename}", "Helvetica", 10)
    y -= 6

    write_wrapped_text("Required Skills / Job Description:", career_goal)

    write_line("Parsed Resume Details", "Helvetica-Bold", 12)
    write_line(f"Name: {parsed_resume.get('name', 'Not found')}")
    write_line(f"Email: {parsed_resume.get('email', 'Not found')}")
    write_line(f"Phone: {parsed_resume.get('phone', 'Not found')}")
    y -= 6

    write_line("ATS Analysis", "Helvetica-Bold", 12)
    write_line(f"ATS Score: {ats_score}/100")
    write_line(f"Contact Details Score: {ats_breakdown.get('contact_score', 0)}/20")
    write_line(f"Skills Score: {ats_breakdown.get('skills_score', 0)}/15")
    write_line(f"Content Quality Score: {ats_breakdown.get('content_quality_score', 0)}/15")
    write_line(f"Section Presence Score: {ats_breakdown.get('section_presence_score', 0)}/20")
    write_line(f"Role Alignment Score: {ats_breakdown.get('alignment_score', 0)}/15")
    write_line(f"Professional Writing Score: {ats_breakdown.get('writing_score', 0)}/15")
    y -= 6

    write_list("ATS Remarks", ats_remarks)
    write_list("Target Skills", target_skills)
    write_list("Matched Skills", matched_skills)
    write_list("Missing Skills", missing_skills)

    write_line(f"Match Percentage: {match_percentage}%", "Helvetica-Bold", 11)
    y -= 8

    write_wrapped_text("Analysis Summary:", analysis_summary)

    write_list("Resume Improvement Suggestions", suggestions.get("resume", []))
    write_list("Skill Development Suggestions", suggestions.get("skill", []))
    write_list("Interview Preparation Suggestions", suggestions.get("interview", []))
    write_list("Generated Interview Questions", interview_questions)

    c.save()
    return output_path