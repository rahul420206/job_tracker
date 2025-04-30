from app.database import get_db

def create_job(title, description, location, company, posted_by):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO jobs (title, description, location, company, posted_by)
        VALUES (%s, %s, %s, %s, %s)''',
        (title, description, location, company, posted_by)
    )
    db.commit()
    return cursor.lastrowid

def get_all_jobs():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs")
    return cursor.fetchall()

def get_jobs_by_recruiter(username):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs WHERE posted_by = %s", (username,))
    return cursor.fetchall()
