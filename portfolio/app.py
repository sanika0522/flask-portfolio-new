from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contacts(name, email, message) VALUES (?, ?, ?)",
            (name, email, message),
        )
        conn.commit()
        conn.close()

        return render_template("contact.html", success=True)

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)