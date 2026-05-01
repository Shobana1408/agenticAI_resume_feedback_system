import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Shobanasql_14",
        database="agentic_resume_db",
        cursorclass=pymysql.cursors.DictCursor
    )