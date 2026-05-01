def generate_interview_questions(role, missing_skills, difficulty="Easy", question_count=5):
    questions = []

    if difficulty == "Easy":
        questions.append(f"Why do you want to become a {role}?")
        questions.append("Tell me about yourself.")
        questions.append("Explain your most important project in simple words.")
        for skill in missing_skills[:3]:
            questions.append(f"What do you know about {skill}?")

    elif difficulty == "Medium":
        questions.append(f"What skills are important for a {role}?")
        questions.append("Explain one project where you solved a technical problem.")
        questions.append("How have you improved your technical skills over time?")
        for skill in missing_skills[:3]:
            questions.append(f"How would you use {skill} in a practical project?")
            questions.append(f"What steps will you take to improve your knowledge in {skill}?")

    elif difficulty == "Hard":
        questions.append(f"How would you prepare yourself technically for a {role} position?")
        questions.append("Explain a challenging technical problem and how you would solve it.")
        questions.append("How would you handle a project task if you are missing an important skill?")
        for skill in missing_skills[:3]:
            questions.append(f"Explain an advanced use case of {skill}.")
            questions.append(f"How would you apply {skill} in a real-world scenario?")

    if len(questions) > question_count:
        questions = questions[:question_count]

    return questions