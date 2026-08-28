"""
+app.py
Student Feedback Ledger — a small Flask + SQLite app for collecting
and reviewing student feedback on courses and teachers.
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

from database import get_connection, init_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ledger-dev-secret-change-me")

# --- Demo admin credentials -------------------------------------------------
# In a real deployment this would live in the database with a proper
# user table. Kept simple here so the project runs out of the box.
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("admin123")


def admin_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


# --- Public routes -----------------------------------------------------------

@app.route("/")
def home():
    conn = get_connection()
    stats = conn.execute(
        "SELECT COUNT(*) AS total, AVG(rating) AS avg_rating FROM feedback"
    ).fetchone()
    teacher_count = conn.execute("SELECT COUNT(*) AS c FROM teachers").fetchone()["c"]
    conn.close()
    return render_template(
        "home.html",
        total=stats["total"] or 0,
        avg_rating=round(stats["avg_rating"], 2) if stats["avg_rating"] else 0,
        teacher_count=teacher_count,
    )


@app.route("/submit", methods=["GET", "POST"])
def submit_feedback():
    conn = get_connection()
    teachers = conn.execute("SELECT * FROM teachers ORDER BY name").fetchall()

    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        roll_no = request.form.get("roll_no", "").strip()
        teacher_id = request.form.get("teacher_id", "")
        course = request.form.get("course", "").strip()
        rating = request.form.get("rating", "")
        comments = request.form.get("comments", "").strip()

        errors = []
        if not student_name:
            errors.append("Please enter your name.")
        if not roll_no:
            errors.append("Please enter your roll number.")
        if not teacher_id:
            errors.append("Please select a teacher.")
        if not course:
            errors.append("Please enter the course name.")
        if rating not in {"1", "2", "3", "4", "5"}:
            errors.append("Please choose a star rating.")

        if errors:
            for e in errors:
                flash(e, "error")
            conn.close()
            return render_template("submit_feedback.html", teachers=teachers, form=request.form)

        conn.execute(
            """INSERT INTO feedback
               (student_name, roll_no, teacher_id, course, rating, comments, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (student_name, roll_no, int(teacher_id), course, int(rating), comments,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("thank_you"))

    conn.close()
    return render_template("submit_feedback.html", teachers=teachers, form={})


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


# --- Admin auth ---------------------------------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["is_admin"] = True
            return redirect(url_for("dashboard"))
        flash("Incorrect username or password.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("home"))


# --- Admin dashboard ------------------------------------------------------

@app.route("/admin/dashboard")
@admin_required
def dashboard():
    conn = get_connection()

    rows = conn.execute("""
        SELECT feedback.*, teachers.name AS teacher_name, teachers.department AS department
        FROM feedback
        JOIN teachers ON teachers.id = feedback.teacher_id
        ORDER BY feedback.created_at DESC
    """).fetchall()

    teachers = conn.execute("SELECT * FROM teachers ORDER BY name").fetchall()

    total = len(rows)
    avg_rating = round(sum(r["rating"] for r in rows) / total, 2) if total else 0

    distribution = {n: 0 for n in range(1, 6)}
    for r in rows:
        distribution[r["rating"]] += 1

    per_teacher = {}
    for r in rows:
        key = r["teacher_name"]
        per_teacher.setdefault(key, {"count": 0, "sum": 0})
        per_teacher[key]["count"] += 1
        per_teacher[key]["sum"] += r["rating"]
    teacher_averages = sorted(
        [
            {"name": name, "count": d["count"], "avg": round(d["sum"] / d["count"], 2)}
            for name, d in per_teacher.items()
        ],
        key=lambda x: x["avg"],
        reverse=True,
    )

    conn.close()
    return render_template(
        "dashboard.html",
        rows=rows,
        teachers=teachers,
        total=total,
        avg_rating=avg_rating,
        distribution=distribution,
        teacher_averages=teacher_averages,
    )


@app.route("/admin/teachers/add", methods=["POST"])
@admin_required
def add_teacher():
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()
    subject = request.form.get("subject", "").strip()
    if name and department and subject:
        conn = get_connection()
        conn.execute(
            "INSERT INTO teachers (name, department, subject) VALUES (?, ?, ?)",
            (name, department, subject),
        )
        conn.commit()
        conn.close()
        flash(f"Added {name} to the teacher list.", "success")
    else:
        flash("All teacher fields are required.", "error")
    return redirect(url_for("dashboard"))


# --- JSON API used by dashboard interactivity ---------------------------------

@app.route("/api/feedback/<int:feedback_id>", methods=["DELETE"])
@admin_required
def delete_feedback(feedback_id):
    conn = get_connection()
    conn.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "id": feedback_id})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
