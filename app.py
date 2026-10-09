import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = "habits.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE,
            UNIQUE (habit_id, completed_date)
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    today = date.today().isoformat()
    conn = get_db()
    # LEFT JOINで今日の達成状態(is_completed)を取得
    query = """
        SELECT habits.id, habits.name, completions.id AS is_completed
        FROM habits
        LEFT JOIN completions 
            ON habits.id = completions.habit_id AND completions.completed_date = ?
        ORDER BY habits.id
    """
    habits = conn.execute(query, (today,)).fetchall()
    conn.close()
    return render_template("index.html", habits=habits, today=today)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"].strip()
    if name:
        conn = get_db()
        conn.execute("INSERT INTO habits (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))

@app.route("/toggle/<int:habit_id>", methods=["POST"])
def toggle(habit_id):
    today = date.today().isoformat()
    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM completions WHERE habit_id = ? AND completed_date = ?",
        (habit_id, today)
    ).fetchone()

    if existing:
        conn.execute("DELETE FROM completions WHERE id = ?", (existing["id"],))
    else:
        conn.execute(
            "INSERT INTO completions (habit_id, completed_date) VALUES (?, ?)",
            (habit_id, today)
        )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:habit_id>", methods=["POST"])
def delete(habit_id):
    conn = get_db()
    conn.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
    conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)