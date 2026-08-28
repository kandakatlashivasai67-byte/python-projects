"""
database.py
Handles SQLite connection, schema creation, and seed data
for the Student Feedback Ledger system.
"""
import sqlite3
import os
from datetime import datetime, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(seed=True):
    """Create tables if they do not exist, and optionally seed sample data."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            subject TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            teacher_id INTEGER NOT NULL,
            course TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
            comments TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    """)

    conn.commit()

    cur.execute("SELECT COUNT(*) AS c FROM teachers")
    has_teachers = cur.fetchone()["c"] > 0

    if seed and not has_teachers:
        teachers = [
            ("Dr. Meera Anand", "Computer Science", "Data Structures"),
            ("Prof. Rohan Kulkarni", "Computer Science", "Operating Systems"),
            ("Dr. Sarah Chen", "Mathematics", "Linear Algebra"),
            ("Prof. Imran Sheikh", "Physics", "Electromagnetism"),
            ("Dr. Alice Fernandes", "Humanities", "Technical Communication"),
        ]
        cur.executemany(
            "INSERT INTO teachers (name, department, subject) VALUES (?, ?, ?)",
            teachers,
        )
        conn.commit()

        cur.execute("SELECT id FROM teachers")
        teacher_ids = [row["id"] for row in cur.fetchall()]

        sample_students = [
            ("Ananya Rao", "21CS041"), ("Vikram Singh", "21CS017"),
            ("Priya Menon", "21CS063"), ("Arjun Nair", "21EC022"),
            ("Divya Patel", "21ME005"), ("Karan Verma", "21CS090"),
        ]
        sample_comments_pos = [
            "Explains concepts very clearly with real examples.",
            "Great pace, easy to follow the lectures.",
            "Very approachable during office hours.",
            "Assignments really helped reinforce the material.",
        ]
        sample_comments_mid = [
            "Good content but could slow down a little.",
            "Slides could use more diagrams.",
            "Would appreciate more practice problems.",
        ]
        sample_comments_neg = [
            "Lectures felt rushed near the end of the term.",
            "Hard to get doubts cleared over email.",
        ]

        seeded = []
        base_date = datetime.now() - timedelta(days=40)
        for i in range(24):
            student = random.choice(sample_students)
            teacher_id = random.choice(teacher_ids)
            rating = random.choices([5, 4, 3, 2, 1], weights=[35, 30, 20, 10, 5])[0]
            if rating >= 4:
                comment = random.choice(sample_comments_pos)
            elif rating == 3:
                comment = random.choice(sample_comments_mid)
            else:
                comment = random.choice(sample_comments_neg)
            created = base_date + timedelta(days=random.randint(0, 40), hours=random.randint(0, 23))
            seeded.append((
                student[0], student[1], teacher_id,
                random.choice(["Core Course", "Elective", "Lab"]),
                rating, comment, created.strftime("%Y-%m-%d %H:%M:%S")
            ))

        cur.executemany(
            """INSERT INTO feedback
               (student_name, roll_no, teacher_id, course, rating, comments, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            seeded,
        )
        conn.commit()

    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialised at {DB_PATH}")
