from app.db.database import get_db

def create_application(job_id, username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO applications (job_id, username)
        VALUES (%s, %s)""",
        (job_id, username)
    )
    db.commit()
    return cursor.lastrowid

def get_application_by_user_and_job(username, job_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM applications WHERE username = %s AND job_id = %s",
        (username, job_id)
    )
    return cursor.fetchone()

def get_applications_by_user(username):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM applications WHERE username = %s", (username,)
    )
    return cursor.fetchall()
