from flask import Flask, render_template, url_for
import data_manager

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/question/<question_id>")
def display_a_question(question_id):
    question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    relevant_answers_dicts = data_manager.find_by_id(question_id, data_manager.LIST_OF_ANSWERS)
    return render_template("display_question.html", question=question_dict, answers=relevant_answers_dicts)

if __name__ == '__main__':
    app.run()
