from flask import Flask, render_template, url_for, redirect
import data_manager
from connection import csv_question_headers
from flask import request

app = Flask(__name__)


class server_state:
    actual_sort_column = 'Time'
    actual_sort_direction = 'ascending'
    def toogle_sort_direction():
        if server_state.actual_sort_direction == 'ascending':
            server_state.actual_sort_direction = 'descending'
        else:
            server_state.actual_sort_direction = 'ascending'


@app.route('/')
def index():
    headers = data_manager.LIST_OF_QUESTIONS[0].keys()
    questions = data_manager.LIST_OF_QUESTIONS

    return render_template("index.html", headers=headers, questions=questions)


@app.route("/sort")
def sort_questions():
    sort_question_column = request.args.get('sort_question_column')
    if sort_question_column == None:
        sort_question_column = 'Submission Time'

    if server_state.actual_sort_column == list(data_manager.titles_for_questions_columns.keys())[
        list(data_manager.titles_for_questions_columns.values()).index(sort_question_column)]:
        server_state.toogle_sort_direction()
    else:
        server_state.actual_sort_direction = 'ascending'

    # get key for value in dictionary i.e. for "Time" -> "submission_time"
    server_state.actual_sort_column = list(data_manager.titles_for_questions_columns.keys())[
        list(data_manager.titles_for_questions_columns.values()).index(sort_question_column)]

    data_manager.LIST_OF_QUESTIONS = data_manager.sort_question(list_of_dicts=data_manager.LIST_OF_QUESTIONS, sort_column=server_state.actual_sort_column,
                                         mode=server_state.actual_sort_direction)
    return redirect(url_for("index"))


@app.route("/question/<question_id>")
def display_a_question(question_id):
    question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    relevant_answers_dicts = data_manager.find_by_id(question_id, data_manager.LIST_OF_ANSWERS)
    num_of_questions = len(data_manager.LIST_OF_QUESTIONS)
    prev, next = data_manager.navigate_by_id(question_dict["Id"])
    return render_template("display_question.html", question=question_dict, answers=relevant_answers_dicts,
                            max_num=str(num_of_questions), next=next, prev=prev)


@app.route("/add-question", methods=["GET"])
def add_question_get():
    return render_template("add-question.html")


@app.route("/add-question", methods=["POST"])
def add_question_post():
    pass


if __name__ == "__main__":
    app.run()
