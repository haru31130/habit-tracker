from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    habits = ["読書", "筋トレ", "英語の勉強"]
    return render_template("index.html", habits=habits)

if __name__ == "__main__":
    app.run(debug=True)