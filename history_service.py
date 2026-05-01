from database.db import get_connection
import json

def save_analysis(
    user_email,
    student_name,
    target_role,
    filename,
    ats_score,
    matched_skills,
    missing_skills,
    career_goal="",
    match_percentage=0,
    ats_breakdown=None,
    analysis_summary=""
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO analysis_history
    (
        user_email,
        student_name,
        target_role,
        filename,
        ats_score,
        matched_skills,
        missing_skills,
        career_goal,
        match_percentage,
        ats_breakdown,
        analysis_summary
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        user_email,
        student_name,
        target_role,
        filename,
        ats_score,
        ", ".join(matched_skills),
        ", ".join(missing_skills),
        career_goal,
        match_percentage,
        json.dumps(ats_breakdown) if ats_breakdown else "{}",
        analysis_summary
    ))

    conn.commit()
    cursor.close()
    conn.close()


def update_generated_questions(user_email, filename, target_role, difficulty, question_count, generated_questions):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE analysis_history
    SET question_difficulty = %s,
        question_count = %s,
        generated_questions = %s
    WHERE id = (
        SELECT id FROM (
            SELECT id
            FROM analysis_history
            WHERE user_email = %s AND filename = %s AND target_role = %s
            ORDER BY id DESC
            LIMIT 1
        ) AS temp_table
    )
    """

    cursor.execute(query, (
        difficulty,
        question_count,
        generated_questions,
        user_email,
        filename,
        target_role
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_user_history(user_email):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM analysis_history WHERE user_email=%s ORDER BY id DESC"
    cursor.execute(query, (user_email,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def delete_selected_history(user_email, history_ids):
    if not history_ids:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(history_ids))
    query = f"""
    DELETE FROM analysis_history
    WHERE user_email = %s AND id IN ({placeholders})
    """

    cursor.execute(query, [user_email] + history_ids)
    conn.commit()

    deleted_count = cursor.rowcount

    cursor.close()
    conn.close()

    return deleted_count


def delete_all_history(user_email):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM analysis_history WHERE user_email = %s"
    cursor.execute(query, (user_email,))
    conn.commit()

    deleted_count = cursor.rowcount

    cursor.close()
    conn.close()

    return deleted_count