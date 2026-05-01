from urllib.parse import quote_plus

CURATED_COURSERA = {
    "Python": {
        "title": "Python for Data Science, AI & Development",
        "url": "https://www.coursera.org/learn/python-for-applied-data-science-ai"
    },
    "SQL": {
        "title": "Data Analysis with Python",
        "url": "https://www.coursera.org/learn/data-analysis-with-python"
    },
    "Machine Learning": {
        "title": "Machine Learning search on Coursera",
        "url": "https://www.coursera.org/courses?query=machine%20learning"
    },
    "Machine Learning Algorithms": {
        "title": "Machine Learning search on Coursera",
        "url": "https://www.coursera.org/courses?query=machine%20learning%20algorithms"
    },
    "Natural Language Processing": {
        "title": "Natural Language Processing search on Coursera",
        "url": "https://www.coursera.org/courses?query=natural%20language%20processing"
    },
    "Data Analysis": {
        "title": "Data Analysis with Python",
        "url": "https://www.coursera.org/learn/data-analysis-with-python"
    },
    "Data Visualization": {
        "title": "Data Visualization search on Coursera",
        "url": "https://www.coursera.org/courses?query=data%20visualization"
    },
    "Statistics": {
        "title": "Statistics search on Coursera",
        "url": "https://www.coursera.org/courses?query=statistics"
    },
    "Excel": {
        "title": "Excel search on Coursera",
        "url": "https://www.coursera.org/courses?query=excel"
    },
    "Power BI": {
        "title": "Power BI search on Coursera",
        "url": "https://www.coursera.org/courses?query=power%20bi"
    },
    "Tableau": {
        "title": "Tableau search on Coursera",
        "url": "https://www.coursera.org/courses?query=tableau"
    },
    "Prompt Engineering": {
        "title": "Prompt Engineering search on Coursera",
        "url": "https://www.coursera.org/courses?query=prompt%20engineering"
    },
    "LLM Integration": {
        "title": "Large Language Models search on Coursera",
        "url": "https://www.coursera.org/courses?query=large%20language%20models"
    },
    "API Integration": {
        "title": "API search on Coursera",
        "url": "https://www.coursera.org/courses?query=api%20integration"
    },
    "Workflow Automation": {
        "title": "Automation search on Coursera",
        "url": "https://www.coursera.org/courses?query=workflow%20automation"
    },
    "Generative Modeling": {
        "title": "Generative AI search on Coursera",
        "url": "https://www.coursera.org/courses?query=generative%20ai"
    },
    "Problem Solving": {
        "title": "Problem Solving search on Coursera",
        "url": "https://www.coursera.org/courses?query=problem%20solving"
    },
    "Git": {
        "title": "Git search on Coursera",
        "url": "https://www.coursera.org/courses?query=git"
    },
    "GitHub": {
        "title": "GitHub search on Coursera",
        "url": "https://www.coursera.org/courses?query=github"
    },
    "Java": {
        "title": "Java search on Coursera",
        "url": "https://www.coursera.org/courses?query=java"
    },
    "JavaScript": {
        "title": "JavaScript search on Coursera",
        "url": "https://www.coursera.org/courses?query=javascript"
    },
    "HTML": {
        "title": "HTML search on Coursera",
        "url": "https://www.coursera.org/courses?query=html"
    },
    "CSS": {
        "title": "CSS search on Coursera",
        "url": "https://www.coursera.org/courses?query=css"
    },
    "React": {
        "title": "React search on Coursera",
        "url": "https://www.coursera.org/courses?query=react"
    },
    "Flutter": {
        "title": "Flutter search on Coursera",
        "url": "https://www.coursera.org/courses?query=flutter"
    },
    "Dart": {
        "title": "Dart search on Coursera",
        "url": "https://www.coursera.org/courses?query=dart"
    },
    "Firebase": {
        "title": "Firebase search on Coursera",
        "url": "https://www.coursera.org/courses?query=firebase"
    },
    "LangChain": {
        "title": "LangChain search on Coursera",
        "url": "https://www.coursera.org/courses?query=langchain"
    },
    "LangGraph": {
        "title": "LangGraph search on Coursera",
        "url": "https://www.coursera.org/courses?query=langgraph"
    },
    "RAG Pipelines": {
        "title": "RAG search on Coursera",
        "url": "https://www.coursera.org/courses?query=retrieval%20augmented%20generation"
    }
}

def get_course_recommendations(missing_skills):
    recommendations = []

    for skill in missing_skills:
        if skill in CURATED_COURSERA:
            recommendations.append({
                "skill": skill,
                "course_title": CURATED_COURSERA[skill]["title"],
                "course_url": CURATED_COURSERA[skill]["url"]
            })
        else:
            search_url = f"https://www.coursera.org/courses?query={quote_plus(skill)}"
            recommendations.append({
                "skill": skill,
                "course_title": f"{skill} search on Coursera",
                "course_url": search_url
            })

    return recommendations