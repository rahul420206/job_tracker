# app/database.py
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="job_tracker"
)
cursor = conn.cursor(dictionary=True)
