# Feedback Ledger — Student Feedback Management System

A small Flask + SQLite app for collecting student feedback on courses and
teachers, and reviewing it from an admin dashboard. Styled as a "gradebook
ledger" — ruled paper, a red notebook margin line, and a rotated grade stamp.

## Stack
- **Backend:** Python (Flask), sqlite3 (standard library, no ORM)
- **Frontend:** server-rendered HTML templates (Jinja2) + vanilla CSS/JS
- **Database:** SQLite (`feedback.db`, created automatically on first run)

## Features

**Student-facing**
- Home page with live stats (entries logged, average rating, teacher count)
- Feedback form: name, roll number, teacher, course type, 1–5 star rating
  (works with or without JS), comments with a live character counter
- Server-side validation with inline flash messages
- Thank-you confirmation page

**Admin dashboard** (`/admin/login`, demo credentials `admin` / `admin123`)
- Summary stat cards, an animated rating-distribution bar chart, and
  average rating per teacher
- Add new teachers to the roster inline
- Ledger table with live search, filter by teacher/rating, click-to-sort
  columns, and delete-with-confirmation (via a small JSON API + fetch)
- Toast notifications for actions

## Setup

```bash
cd student-feedback-system
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

The SQLite database (`feedback.db`) is created automatically the first time
you run the app, seeded with a handful of sample teachers and feedback
entries so the dashboard isn't empty on first look. Delete `feedback.db` and
restart the app any time to reset to a fresh, re-seeded database.

## Project structure

```
student-feedback-system/
├── app.py                  # Flask routes
├── database.py             # SQLite schema + seed data
├── requirements.txt
├── feedback.db              # created on first run
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/
    ├── base.html
    ├── home.html
    ├── submit_feedback.html
    ├── thank_you.html
    ├── admin_login.html
    └── dashboard.html
```

## Notes for extending this

- Admin credentials are hardcoded in `app.py` for demo purposes — swap in a
  real `users` table with hashed passwords before deploying this anywhere.
- `app.secret_key` should be set via an environment variable in production
  (`SECRET_KEY`), not the fallback dev value.
- The delete endpoint (`/api/feedback/<id>`) is a good template for adding
  more JSON endpoints (e.g. an edit-teacher API) if you want the dashboard
  to do more without full page reloads.
