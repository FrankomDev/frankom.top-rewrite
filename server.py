from flask import Flask, render_template, request, redirect, session, jsonify
import database as db
import login as lgn
import files as fl
import os

app = Flask(__name__)
app.secret_key = os.getenv("PASSWORD")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hardware")
def hardware():
    return render_template("hardware.html")

@app.route("/links")
def links():
    return render_template("links.html")

@app.route("/blog", methods={"GET", "POST"})
def blog():
    if request.method == "GET":
        if request.args.get("api"):
            return blog.get_data()
        else:
            return render_template("blog.html", data=blog.get_data())
    elif request.method == "POST":
        if session.get("admin"):
            try:
                title = request.form["title"]
                content = request.form["content"]
                if title and content:
                    blog.post_blog(title, content)
                    return redirect("/blog", code=302)
            except Exception:
                pass
        return "nah", 418

@app.route("/blog/<id>", methods={"GET", "DELETE", "POST"})
def blog_post(id):
    if request.method == "GET":
        try:
            if request.args.get("api"):
                return jsonify(blog.get_content(id))
            else:
                return render_template("empty.html", data=blog.get_content(id))
        except Exception:
            return render_template("empty.html", data="")
    elif request.method == "DELETE":
        if session.get("admin"):
            blog.remove_content(id)
            return "ok"
    elif request.method == "POST":
        if session.get("admin"):
            try:
                title = request.form["title"]
                content = request.form["content"]
                if title and content:
                    blog.update_content(id, title, content)
            except Exception:
                pass
            return render_template("empty.html", data=blog.get_content(id))
    return "nah", 418

@app.route("/guestbook", methods={"GET", "POST"})
def guestbook():
    if request.method == "GET":
        if request.args.get("api"):
            return guestbook.get_data()
        else:
            return render_template("guestbook.html", data=guestbook.get_data())
    elif request.method == "POST":
        try:
            username = request.form["username"]
            message = request.form["message"]
            if username and message:
                guestbook.post_message(username, message)
        except Exception:
            pass
        return redirect("/guestbook", code=302)

@app.route("/guestbook/<id>", methods={"DELETE"})
def del_guestbook(id):
    if session.get("admin"):
        guestbook.remove_content(id)
        return "ok"
    return "nah", 418

@app.route("/projects", methods={"GET", "POST"})
def projects():
    if request.method == "GET":
        if request.args.get("api"):
            return projects.get_data()
        else:
            return render_template("projects.html", data=projects.get_data())
    elif request.method == "POST":
        if session.get("admin"):
            try:
                title = request.form["title"]
                content = request.form["content"]
                if title and content:
                    projects.post_project(title, content)
                    return redirect("/projects", code=302)
            except Exception:
                pass
        return "nah", 418

@app.route("/projects/<id>", methods={"GET", "DELETE", "POST"})
def project(id):
    if request.method == "GET":
        try:
            if request.args.get("api"):
                return jsonify(projects.get_content(id))
            else:
                return render_template("empty.html", data=projects.get_content(id))
        except Exception:
            return render_template("empty.html", data="")
    elif request.method == "DELETE":
        if session.get("admin"):
            projects.remove_content(id)
            return "ok"
    elif request.method == "POST":
        if session.get("admin"):
            try:
                title = request.form["title"]
                content = request.form["content"]
                if title and content:
                    projects.update_content(id, title, content)
            except Exception:
                pass
            return render_template("empty.html", data=projects.get_content(id))
    return "nah", 418

@app.route("/admin", methods={"GET", "POST"})
def login():
    if request.method == "GET":
        if session.get("admin"):
            return render_template("admin/admin.html")
        return render_template("login.html")
    elif request.method == "POST":
        try:
            password = request.form["password"]
            if password:
                if login.try_login(password):
                    session["admin"] = True
                    return render_template("admin/admin.html")
        except Exception:
            pass
        return redirect("/admin", code=302)

@app.route("/files", methods={"GET", "POST"})
def files():
    if request.method == "GET":
        if session.get("admin"):
            return files.get()
        return "nah", 418
    elif request.method == "POST":
        if 'file' in request.files and session.get("admin"):
            files.upload(request.files['file'])
            return redirect("/admin", code=302)
        return "nah", 418

@app.route("/files/<name>", methods={"DELETE"})
def file_del(name):
    if session.get("admin"):
        files.delete(name)
        return "ok"
    return "nah", 418

guestbook = db.Guestbook()
projects = db.Projects()
blog = db.Blog_posts()
login = lgn.Login()
files = fl.Files()
#app.run()
