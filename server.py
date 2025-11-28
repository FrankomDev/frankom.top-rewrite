from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hardware")
def hardware():
    return render_template("hardware.html")

@app.route("/blog")
def blog():
    return "WIP"

@app.route("/socials")
def socials():
    return "WIP"

if __name__ == "__main__":
    app.run(debug=True)