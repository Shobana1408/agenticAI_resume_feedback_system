def format_skill_list(skills):
    if not skills:
        return ""

    if len(skills) == 1:
        return skills[0]

    if len(skills) == 2:
        return f"{skills[0]} and {skills[1]}"

    return ", ".join(skills[:-1]) + f", and {skills[-1]}"


def generate_feedback(missing_skills, ats_remarks):
    resume_suggestions = []
    skill_suggestion = ""
    interview_suggestion = ""

    for remark in ats_remarks:
        if remark not in resume_suggestions:
            resume_suggestions.append(remark)

    if missing_skills:
        skill_text = format_skill_list(missing_skills)
        skill_suggestion = (
            f"To improve your profile for the target role, focus on learning or strengthening "
            f"{skill_text}."
        )
        interview_suggestion = (
            f"You should prepare for interview questions related to {skill_text}."
        )
    else:
        skill_suggestion = (
            "Your skill profile is well aligned with the target role, so focus on revising your existing strengths and project explanations."
        )
        interview_suggestion = (
            "Focus on revising your existing technical strengths, project explanations, and problem-solving approach for interviews."
        )

    if not resume_suggestions:
        resume_suggestions.append("Your resume is in good shape, but it can still be improved further with clearer structure and stronger role alignment.")

    return {
        "resume": " ".join(resume_suggestions),
        "skill": skill_suggestion,
        "interview": interview_suggestion
    }