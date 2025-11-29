from flask import Flask, render_template
import sqlite3

def configure_db() -> None:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS blog (id num, date text, title text, content text)")
    conn.commit()
    conn.close()

def get_posts() -> list:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    posts = cursor.execute("SELECT date, title, id FROM blog ORDER BY id DESC").fetchall()
    conn.close()
    return posts

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hardware")
def hardware():
    return render_template("hardware.html")

@app.route("/blog")
def blog():
    return render_template("blog.html", posts=get_posts())

@app.route("/blog/<int:id>")
def blog_post(id):
    return str(id)

@app.route("/socials")
def socials():
    return "WIP"

if __name__ == "__main__":
    configure_db()
    app.run(debug=True)