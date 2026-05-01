def generate_analysis_summary(role, ats_score, missing_skills, match_percentage):
    if ats_score >= 80:
        ats_text = "Your resume shows good ATS readiness."
    elif ats_score >= 60:
        ats_text = "Your resume has moderate ATS readiness and can be improved further."
    else:
        ats_text = "Your resume needs improvement in ATS readiness."

    if len(missing_skills) == 0:
        skill_text = f"Your profile is well aligned with the {role} role."
    else:
        top_missing = ", ".join(missing_skills[:3])
        skill_text = f"You are currently missing {len(missing_skills)} important skills for the {role} role, such as {top_missing}."

    match_text = f"Your current skill match is {match_percentage}%."

    return f"{ats_text} {skill_text} {match_text}"