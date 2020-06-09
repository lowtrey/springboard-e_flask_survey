from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

# Initialize App & Variables
app = Flask(__name__)
survey = surveys["personality"]

# Configure Key for Session
app.config["SECRET_KEY"] = "oh-so-secret"
# Turn off Redirect Intercept
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# instantiate toolbar
debug = DebugToolbarExtension(app)


# Handle root route - render survey
@app.route("/")
def start_survey():
    """Show survey page"""
    
    return render_template("home.html", survey=survey)


# Start Session and Redirect
@app.route("/session", methods=["POST"])
def start_session():
    """Initialize response list and redirect to first question"""

    session["responses"] = []

    return redirect("/questions/0")


# Handle Question Routes
@app.route("/questions/<int:question_number>")
def show_question(question_number):
    """Show question with provided index"""

    responses = session.get("responses", [])

    if question_number != len(responses):

        flash("Questions must be answered in order.", "error")

        return redirect(f"/questions/{len(responses)}")

    elif len(responses) < len(survey.questions):

        question = survey.questions[question_number].question

        choices = survey.questions[question_number].choices

        return render_template("questions.html", num=question_number, question=question, choices=choices)

    else:

        return redirect("/thanks")


# Handle Answer Routes
@app.route("/answer", methods=["POST"])
def show_answer():
    """Show answer page"""

    responses = session.get("responses", [])

    answer = request.form.get("choice")

    responses.append(answer)

    session["responses"] = responses

    next_question_index = len(responses)

    if len(responses) < len(survey.questions):

        return redirect(f"/questions/{next_question_index}")

    else:

        return redirect("/thanks")


# Handle Thank You Route
@app.route("/thanks")
def thank_user():
    """Show thank you page"""
    
    return render_template("thank_you.html")