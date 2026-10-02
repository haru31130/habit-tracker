import sqlite3
from flask import Flask, render_template

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

if __name__ == "__main__":
    init_db()
    app.run(debug=True)