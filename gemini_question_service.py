import time
from google import genai

def _extract_questions(text, question_count):
    questions = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        if line[0].isdigit():
            parts = line.split(".", 1)
            if len(parts) == 2:
                questions.append(parts[1].strip())
            else:
                questions.append(line)
        else:
            questions.append(line)

    return questions[:question_count]

def generate_questions_with_gemini(api_key, role, missing_skills, difficulty, question_count, career_goal):
    client = genai.Client(api_key=api_key)

    missing_text = ", ".join(missing_skills) if missing_skills else "no major missing skills"

    prompt = f"""
You are helping a student prepare for interviews.

Target role: {role}
Career goal: {career_goal}
Missing skills: {missing_text}
Difficulty level: {difficulty}
Number of questions needed: {question_count}

Generate exactly {question_count} interview questions.
The questions must match the selected difficulty.
Return only the questions as a numbered list.
Do not add explanations.
"""

    models_to_try = [
        "gemini-2.5-flash",
        "gemini-1.5-flash"
    ]

    last_error = None

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                text = response.text.strip()
                questions = _extract_questions(text, question_count)

                if questions:
                    return questions

            except Exception as e:
                last_error = e
                time.sleep(2)

    raise Exception(f"Gemini service temporarily unavailable. Please try again. Details: {last_error}")