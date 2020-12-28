from flask import Flask, render_template, url_for
import data_manager, connection
app = Flask(__name__)


@app.route('/')
def index():
    headers = data_manager.LIST_OF_QUESTIONS[0].keys()
    questions = data_manager.LIST_OF_QUESTIONS  # lista powinna zostać posortowana, rozwiązanie tymczasowe
    # sort_column = connection.csv_question_headers.submission_time
    # questions = data_manager.sort_question(data_manager.LIST_OF_QUESTIONS, sort_column)
    return render_template("index.html", headers=headers, questions=questions)


@app.route("/question/<question_id>")
def display_a_question(question_id):
    question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    relevant_answers_dicts = data_manager.find_by_id(question_id, data_manager.LIST_OF_ANSWERS)
    return render_template("display_question.html", question=question_dict, answers=relevant_answers_dicts)


if __name__ == '__main__':
    app.run()

