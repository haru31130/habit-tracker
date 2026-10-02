import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = "habits.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
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
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    habits = conn.execute("SELECT * FROM habits ORDER BY id").fetchall()
    conn.close()
    return render_template("index.html", habits=habits)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"].strip()
    if name:
        conn = get_db()
        conn.execute("INSERT INTO habits (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:habit_id>", methods=["POST"])
def delete(habit_id):
    conn = get_db()
    conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)