from flask import Flask, render_template, url_for
import data_manager

app = Flask(__name__)


# @app.route("/")
# def hello():
#     return "Hello World!"


@app.route('/')
def index():
    questions_column = data_manager.titles_for_questions_columns
    stories = data_manager.LIST_OF_QUESTIONS
    return render_template("index.html", headers=questions_column, stories=stories)

@app.route("/question/<question_id>")
def display_a_question(question_id):
    question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    relevant_answers_dicts = data_manager.find_by_id(question_id, data_manager.LIST_OF_ANSWERS)
    num_of_questions = len(data_manager.LIST_OF_QUESTIONS)
    prev, next = data_manager.navigate_by_id(question_dict["id"])
    return render_template("display_question.html", question=question_dict, answers=relevant_answers_dicts,
                            max_num=str(num_of_questions), next=next, prev=prev)


if __name__ == "__main__":
    app.run()
