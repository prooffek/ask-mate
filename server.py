from flask import Flask, render_template, url_for, redirect, request
import data_manager, util, connection
from connection import csv_question_headers


app = Flask(__name__)


class server_state:
    actual_sort_column = 'Submission Time'
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

    return render_template("index.html", headers=headers, questions=questions, server_state=server_state)


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


@app.route("/vote", methods=["POST"])
def vote():
    question_id = request.form.get("question_id")
    vote_type = request.form.get("vote")

    question = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)
    question_index = data_manager.LIST_OF_QUESTIONS.index(question[0])

    if vote_type == "up_vote":
        data_manager.LIST_OF_QUESTIONS[question_index]["Vote Number"] = int(data_manager.LIST_OF_QUESTIONS[question_index]["Vote Number"]) + 1
    else:
        data_manager.LIST_OF_QUESTIONS[question_index]["Vote Number"] = int(data_manager.LIST_OF_QUESTIONS[question_index]["Vote Number"]) - 1
    data_manager.update_questions()

    return redirect(url_for("index"))





@app.route("/question/<question_id>")
def display_a_question(question_id):
    question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    relevant_answers_dicts = data_manager.find_by_id(question_id, data_manager.LIST_OF_ANSWERS)
    return render_template("display_question.html", question=question_dict, answers=relevant_answers_dicts)
    # question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    # relevant_answers_dicts = data_manager.find_by_id(question_id, data_manager.LIST_OF_ANSWERS)
    # num_of_questions = len(data_manager.LIST_OF_QUESTIONS)
    # prev, next = data_manager.navigate_by_id(question_dict["Id"])
    # return render_template("display_question.html", question=question_dict, answers=relevant_answers_dicts,
    #                         max_num=str(num_of_questions), next=next, prev=prev)


@app.route("/add-question", methods=["GET"])
def add_question_get():
    return render_template("add-question.html")


@app.route("/add-question", methods=["POST"])
def add_question_post():
    data_from_form = dict(request.form)
    new_question = {
        "Id": str(data_manager.next_id(data_manager.LIST_OF_QUESTIONS)),
        "Submission Time": str(util.convert_date_to_timestamp(util.current_datetime())),
        "View Number": "0",
        "Vote Number": "0",
        "Title": data_from_form["Title"],
        "Message": data_from_form["Message"],
        "Image": ""
    }
    data_manager.LIST_OF_QUESTIONS.append(new_question)
    connection.append_to_file("question.csv", new_question)
    return redirect(url_for("display_a_question", question_id=new_question["Id"]))


@app.route("/question/<question_id>/new_answer", methods=["GET"])
def post_an_answer_get(question_id):
    question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    return render_template("add-question.html", question_id=question_id, question=question_dict)


@app.route("/question/<question_id>/new_answer", methods=["POST"])
def post_an_answer_post(question_id):
    new_answer = {
        "Id": data_manager.next_id(data_manager.LIST_OF_ANSWERS),
        "Submission Time": util.todays_date(),
        "Vote Number": 0
    }

    new_answer.update(request.form)
    data_manager.update_answer_list(new_answer)
    return redirect(url_for("display_a_question", question_id=question_id))


if __name__ == "__main__":
    app.run()
