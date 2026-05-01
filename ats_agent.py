import re

def calculate_ats_score(parsed_resume, target_skills=None, matched_skills=None):
    remarks = []

    contact_score = 0
    skills_score = 0
    content_quality_score = 0
    section_presence_score = 0
    alignment_score = 0
    writing_score = 0

    resume_text = parsed_resume.get("resume_text", "")
    resume_text_lower = resume_text.lower()
    resume_skills = parsed_resume.get("skills", [])

    # Contact Details Score /20
    if parsed_resume.get("name") != "Not found":
        contact_score += 7
    else:
        remarks.append("Name is missing.")

    if parsed_resume.get("email") != "Not found":
        contact_score += 7
    else:
        remarks.append("Email is missing.")

    if parsed_resume.get("phone") != "Not found":
        contact_score += 6
    else:
        remarks.append("Phone number is missing.")

    if contact_score >= 18:
        remarks.append("Contact details are mostly complete.")

    # Skills Score /15
    skill_count = len(resume_skills)
    if skill_count >= 8:
        skills_score = 15
        remarks.append("Resume contains a strong number of technical skills.")
    elif skill_count >= 5:
        skills_score = 12
        remarks.append("Resume contains a moderate number of technical skills.")
    elif skill_count >= 3:
        skills_score = 8
        remarks.append("Add more relevant technical skills to strengthen the resume.")
    elif skill_count >= 1:
        skills_score = 5
        remarks.append("Very few skills are listed. Add more role-related skills.")
    else:
        skills_score = 0
        remarks.append("Skills section appears weak or missing.")

    # Content Quality Score /15
    text_length = len(resume_text.strip())
    if text_length > 800:
        content_quality_score = 15
        remarks.append("Resume content is detailed.")
    elif text_length > 500:
        content_quality_score = 12
        remarks.append("Resume content is reasonably detailed.")
    elif text_length > 250:
        content_quality_score = 8
        remarks.append("Resume content can be improved with stronger details.")
    elif text_length > 0:
        content_quality_score = 4
        remarks.append("Resume content is too short.")
    else:
        content_quality_score = 0
        remarks.append("Resume text is unavailable for full analysis.")

    # Section Presence Score /20
    if "education" in resume_text_lower:
        section_presence_score += 5
    else:
        remarks.append("Education section is missing.")

    if "skills" in resume_text_lower or "technical skills" in resume_text_lower:
        section_presence_score += 5
    else:
        remarks.append("Skills section heading is missing.")

    if "project" in resume_text_lower or "projects" in resume_text_lower:
        section_presence_score += 5
    else:
        remarks.append("Projects section is missing.")

    if "experience" in resume_text_lower or "internship" in resume_text_lower or "work experience" in resume_text_lower:
        section_presence_score += 5
    else:
        remarks.append("Experience or internship section is missing.")

    if section_presence_score == 20:
        remarks.append("Important resume sections are present.")

    # Role Alignment Score /15
    if target_skills is not None and matched_skills is not None and len(target_skills) > 0:
        ratio = len(matched_skills) / len(target_skills)

        if ratio >= 0.8:
            alignment_score = 15
            remarks.append("Resume is strongly aligned with the selected target role.")
        elif ratio >= 0.6:
            alignment_score = 11
            remarks.append("Resume has moderate alignment with the selected target role.")
        elif ratio >= 0.4:
            alignment_score = 7
            remarks.append("Resume has partial alignment with the selected target role.")
        else:
            alignment_score = 3
            remarks.append("Resume has low alignment with the selected target role.")
    else:
        remarks.append("Target-role alignment could not be evaluated fully.")

    # Professional Writing Score /15
    weak_phrases = [
        "i want job",
        "i am student",
        "it is cool",
        "some udemy courses",
        "some coding",
        "i know some",
        "nothing much",
        "maybe",
        "not sure",
        "i think",
        "sometimes",
        "will share later",
        "and all",
        "mostly",
        "trying my best",
        "somewhere",
        "heard about it",
        "basic i think",
        "want to do",
        "cool",
        "good at badminton"
    ]

    weak_count = 0
    for phrase in weak_phrases:
        if phrase in resume_text_lower:
            weak_count += 1

    # Poor capitalization checks
    lowercase_i_count = len(re.findall(r"\bi\b", resume_text))
    all_lowercase_heading_count = 0

    possible_headings = [
        "objective", "education", "experience", "skills",
        "technical skills", "projects", "certifications"
    ]
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    for line in lines:
        if line in possible_headings:
            all_lowercase_heading_count += 1

    weak_objective = False
    if "objective" in resume_text_lower:
        objective_patterns = [
            "i want job",
            "i am student",
            "it is cool",
            "i know some coding"
        ]
        for pattern in objective_patterns:
            if pattern in resume_text_lower:
                weak_objective = True
                break

    penalty_score = 0
    penalty_score += weak_count * 2
    penalty_score += min(lowercase_i_count, 3)
    penalty_score += min(all_lowercase_heading_count, 3)

    if weak_objective:
        penalty_score += 2

    writing_score = 15 - penalty_score

    if writing_score < 2:
        writing_score = 2

    if writing_score >= 13:
        remarks.append("Writing style is professional and clear.")
    elif writing_score >= 10:
        remarks.append("Writing style is acceptable but can be more professional.")
    elif writing_score >= 7:
        remarks.append("Resume writing has some weak or informal wording.")
    elif writing_score >= 4:
        remarks.append("Resume contains informal wording and should be written more professionally.")
    else:
        remarks.append("Resume writing style is highly informal and needs strong improvement.")

    total_score = (
        contact_score
        + skills_score
        + content_quality_score
        + section_presence_score
        + alignment_score
        + writing_score
    )

    if total_score > 100:
        total_score = 100

    breakdown = {
        "contact_score": contact_score,
        "skills_score": skills_score,
        "content_quality_score": content_quality_score,
        "section_presence_score": section_presence_score,
        "alignment_score": alignment_score,
        "writing_score": writing_score
    }

    return total_score, remarks, breakdown