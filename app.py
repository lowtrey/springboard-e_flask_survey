from flask import Flask, render_template, request, redirect
from surveys import surveys

app = Flask(__name__)
survey = surveys["satisfaction"]
responses = []


# Handle root route - render survey
@app.route("/")
def start_survey():
    return render_template("home.html", survey=survey)


# Handle Question Routes
@app.route("/questions/<int:question_number>")
def ask_question(question_number):
    if question_number >= 0 and question_number < len(survey.questions):
        question = survey.questions[question_number].question
        choices = survey.questions[question_number].choices
        return render_template("questions.html", num=question_number, question=question, choices=choices)
    else:
        return "Question not found..."


# Handle Answer Routes
@app.route("/answer", methods=["POST"])
def show_answer():
    answer = request.form.get("choice")
    responses.append(answer)
    next_question_index = int(request.form.get("question_number")) + 1
    print(responses)

    if next_question_index < len(survey.questions):
        return redirect(f"/questions/{next_question_index}")
    else:
        return "No more questions"