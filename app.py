from flask import Flask, render_template
from surveys import surveys

app = Flask(__name__)
responses = []


# Handle root route - render survey
@app.route("/")
def start_survey():
    survey = surveys["satisfaction"]
    return render_template("home.html", survey=survey)