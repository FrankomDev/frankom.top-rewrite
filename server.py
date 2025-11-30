from flask import Flask, render_template, request, redirect, make_response
import sqlite3
import random
from datetime import datetime

password : str = ''
tokens : list = []

def read_env() -> None:
    global password
    with open(".env", "r") as f:
        password=f.readline()

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

def get_post_by_id(id : int) -> list:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    posts = cursor.execute("SELECT title, date, content FROM blog WHERE id=?", (id,)).fetchone()
    conn.close()
    return posts

def get_last_id() -> int:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    id = cursor.execute("SELECT id FROM blog ORDER BY id DESC").fetchone()
    conn.close()
    return id[0]

def publish_post(title : str, content : str, id : int) -> None:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    date = datetime.now().strftime("%d %b %Y")
    cursor.execute("INSERT INTO blog VALUES (?, ?, ?, ?)", (id, date, title, content))
    conn.commit()
    conn.close()

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
    return render_template("post.html", post=get_post_by_id(id))

@app.route("/socials")
def socials():
    return render_template("socials.html")

@app.route("/admin", methods=["POST"])
def admin():
    if request.form['passwd'] == password:
        token = random.randint(111111111,999999999)
        tokens.append(str(token))
        resp = make_response(render_template("admin.html"))
        resp.set_cookie("token", str(token))
        return resp
    else:
        return redirect("/blog?e=1")

@app.route("/admin/publish", methods=["POST"])
def publish():
    if request.cookies.get("token") in tokens:
        title = request.form['post-title']
        content = request.form['post-content']
        id = get_last_id()+1
        publish_post(title, content, id)
        tokens.clear()
        return redirect(f"/blog/{id}")
    else:
        return redirect("/blog")

if __name__ == "__main__":
    read_env()
    configure_db()
    app.run(debug=True)