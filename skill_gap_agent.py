import re

KNOWN_SKILLS = [
    "natural language processing",
    "machine learning algorithms",
    "data synthesis techniques",
    "workflow automation",
    "prompt engineering",
    "llm integration",
    "api integration",
    "generative modeling",
    "data visualization",
    "problem solving",
    "machine learning",
    "data structures",
    "object oriented programming",
    "web development",
    "rest api",
    "power bi",
    "tableau",
    "javascript",
    "node.js",
    "python",
    "java",
    "sql",
    "html",
    "css",
    "flask",
    "django",
    "mysql",
    "git",
    "react",
    "excel",
    "statistics",
    "c++",
    "c"
]

def format_skill_name(skill):
    special_map = {
        "sql": "SQL",
        "html": "HTML",
        "css": "CSS",
        "javascript": "JavaScript",
        "c++": "C++",
        "c": "C",
        "mysql": "MySQL",
        "git": "Git",
        "react": "React",
        "node.js": "Node.js",
        "rest api": "REST API",
        "power bi": "Power BI",
        "llm integration": "LLM Integration",
        "api integration": "API Integration",
        "natural language processing": "Natural Language Processing",
        "machine learning algorithms": "Machine Learning Algorithms",
        "data synthesis techniques": "Data Synthesis Techniques",
        "workflow automation": "Workflow Automation",
        "prompt engineering": "Prompt Engineering",
        "generative modeling": "Generative Modeling",
        "data visualization": "Data Visualization",
        "problem solving": "Problem Solving",
        "object oriented programming": "Object Oriented Programming",
        "web development": "Web Development",
        "data structures": "Data Structures",
        "machine learning": "Machine Learning"
    }
    return special_map.get(skill.lower(), skill.title())

def normalize_text(text):
    text = text.lower()
    text = text.replace("-", " ")
    text = text.replace("/", " ")
    return text

def extract_goal_skills(career_goal_text):
    text_lower = normalize_text(career_goal_text)
    found_skills = []

    # Check longer phrases first
    sorted_skills = sorted(KNOWN_SKILLS, key=len, reverse=True)

    for skill in sorted_skills:
        normalized_skill = normalize_text(skill)

        # strict word-boundary match
        pattern = r"\b" + re.escape(normalized_skill) + r"\b"

        if re.search(pattern, text_lower):
            formatted_skill = format_skill_name(skill)
            if formatted_skill not in found_skills:
                found_skills.append(formatted_skill)

    return found_skills

def analyze_skill_gap(resume_skills, career_goal_text):
    target_skills = extract_goal_skills(career_goal_text)

    resume_skill_set = set(resume_skills)
    target_skill_set = set(target_skills)

    matched_skills = list(resume_skill_set.intersection(target_skill_set))
    missing_skills = list(target_skill_set - resume_skill_set)

    if len(target_skill_set) > 0:
        match_percentage = int((len(matched_skills) / len(target_skill_set)) * 100)
    else:
        match_percentage = 0

    return target_skills, matched_skills, missing_skills, match_percentage