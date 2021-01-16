from flask import Flask, render_template, url_for, redirect, request
import data_manager, util, connection, os
import copy
import data_manager_filter


app = Flask(__name__)

LIST_OF_TAGS = data_manager.get_tags_names()

class server_state:
    #SORTING
    actual_sort_column = 'Submission Time'
    actual_sort_direction = 'ascending'

    def toogle_sort_direction():
        if server_state.actual_sort_direction == 'ascending':
            server_state.actual_sort_direction = 'descending'
        else:
            server_state.actual_sort_direction = 'ascending'

    #FILTERING
    actual_advanced_filter_on_date = "no"
    actual_advanced_filter_on_status = "no"
    actual_filter_reset_button_active = "no"
    filter_reset_active = "no"

    default_filter_by_date = "Last month"
    default_filter_by_status = "active"
    default_filter_by_search = ""

    #default values for starting page
    actual_filter_by_date_mode = default_filter_by_date             #valid values: filter_by_date_mode
    actual_filter_by_status_mode = default_filter_by_status         #valid values: filter_by_status_mode
    actual_filter_by_search_mode = default_filter_by_search         #valid values: filter_by_search_mode

    FILTERED_LIST_OF_QUESTIONS = []

    def update_filtered_list_of_questions():
        data_manager.update_questions_statuses(data_manager.LIST_OF_QUESTIONS, data_manager.LIST_OF_ANSWERS)
        data_manager.update_file(data_manager.LIST_OF_QUESTIONS)
        server_state.FILTERED_LIST_OF_QUESTIONS = copy.deepcopy(data_manager.LIST_OF_QUESTIONS)
        filter_question()

    def toogle_advanced_filter_date():
        if server_state.actual_advanced_filter_on_date == "no":
            server_state.actual_advanced_filter_on_date = "yes"
        else:
            server_state.actual_advanced_filter_on_date = "no"

    def toogle_advanced_filter_status():
        if server_state.actual_advanced_filter_on_status == "no":
            server_state.actual_advanced_filter_on_status = "yes"
        else:
            server_state.actual_advanced_filter_on_status = "no"

@app.route('/', methods=["GET"])
def index():
    headers = data_manager.LIST_OF_QUESTIONS[0].keys()

    server_state.update_filtered_list_of_questions()
    questions = server_state.FILTERED_LIST_OF_QUESTIONS

    answers = data_manager.LIST_OF_ANSWERS
    answers_number_for_questions = data_manager.find_answers_number_for_questions(questions, answers)

    return render_template("index.html", headers=headers, questions=questions, server_state=server_state, answers_number=answers_number_for_questions)

@app.route('/', methods=["POST"])
def index_post():
    if request.form.get("actual_advanced_filter_date_clicked") == "clicked":
        server_state.toogle_advanced_filter_date()
        if server_state.actual_advanced_filter_on_status == "yes":
            server_state.toogle_advanced_filter_status()

    if request.form.get("actual_advanced_filter_status_clicked") == "clicked":
        server_state.toogle_advanced_filter_status()
        if server_state.actual_advanced_filter_on_date == "yes":
            server_state.toogle_advanced_filter_date()

    if request.form.get("date_filter_changed") == "true":
        server_state.actual_filter_by_date_mode = request.form.get("date_filter")
        server_state.toogle_advanced_filter_date()

    if request.form.get("status_filter_changed") == "true":
        server_state.actual_filter_by_status_mode = request.form.get("status_filter")
        server_state.toogle_advanced_filter_status()

    if request.form.get("filter_reset_button_clicked") == "clicked":
            server_state.actual_filter_by_date_mode = server_state.default_filter_by_date
            server_state.actual_filter_by_status_mode = server_state.default_filter_by_status
            server_state.actual_filter_by_search_mode = server_state.default_filter_by_search
            server_state.filter_reset_active = "no"

    if not (server_state.actual_filter_by_date_mode == server_state.default_filter_by_date and \
        server_state.actual_filter_by_status_mode == server_state.default_filter_by_status and \
        server_state.actual_filter_by_search_mode == server_state.default_filter_by_search):
            server_state.filter_reset_active = "yes"

    if request.form.get("filter_search_clicked") == "yes":
        server_state.actual_filter_by_search_mode = request.form.get("searched_text")
        server_state.filter_reset_active = "yes"

    return redirect(url_for("filter_question"))

@app.route("/filter")
def filter_question() -> list:
    NEW_FILTERED_LIST_OF_QUESTIONS = copy.deepcopy(data_manager.LIST_OF_QUESTIONS)

    # Three filters apply to list of questions
    #1th filtering by date
    NEW_FILTERED_LIST_OF_QUESTIONS = data_manager_filter.filter_by_date(NEW_FILTERED_LIST_OF_QUESTIONS, server_state.actual_filter_by_date_mode)
    #2nd filtering by status
    NEW_FILTERED_LIST_OF_QUESTIONS = data_manager_filter.filter_by_status(NEW_FILTERED_LIST_OF_QUESTIONS, server_state.actual_filter_by_status_mode)
    #3th filtering by search
    NEW_FILTERED_LIST_OF_QUESTIONS = data_manager_filter.filter_by_search(NEW_FILTERED_LIST_OF_QUESTIONS,\
                                                                          server_state.actual_filter_by_search_mode)
    server_state.FILTERED_LIST_OF_QUESTIONS = copy.deepcopy(NEW_FILTERED_LIST_OF_QUESTIONS)

    return redirect(url_for("index"))

@app.route("/sort")
def sort_questions():
    sort_question_column = request.args.get('sort_question_column')

    if sort_question_column == None:
        sort_question_column = 'Submission Time'

    if not sort_question_column =="Answers":
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
    else:
        if server_state.actual_sort_column == "Answers":
            server_state.toogle_sort_direction()
        else:
            server_state.actual_sort_direction = 'descending'
        server_state.actual_sort_column = "Answers"
        answers_number_for_questions = data_manager.find_answers_number_for_questions(data_manager.LIST_OF_QUESTIONS,
                                                                                      data_manager.LIST_OF_ANSWERS)
        data_manager.LIST_OF_QUESTIONS = data_manager.sort_question_by_answers_number(data_manager.LIST_OF_QUESTIONS, answers_number_for_questions, mode=server_state.actual_sort_direction)
    return redirect(url_for("index"))

@app.route("/vote", methods=["POST"])
def vote():
    question_id = request.form.get("question_id")
    vote_type = request.form.get("vote") # vote_up or vote_down
    url_origin = request.form.get("url_origin")
    vote_for_answer_or_question = request.form.get("vote_for_answer_or_question") # vote_for_answer or vote_for_question

    if vote_for_answer_or_question == "vote_for_question":
        question = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)
        question_index = data_manager.LIST_OF_QUESTIONS.index(question[0])

        if vote_type == "up_vote":
            data_manager.LIST_OF_QUESTIONS[question_index]["Vote Number"] = int(data_manager.LIST_OF_QUESTIONS[question_index]["Vote Number"]) + 1
        else:
            data_manager.LIST_OF_QUESTIONS[question_index]["Vote Number"] = int(data_manager.LIST_OF_QUESTIONS[question_index]["Vote Number"]) - 1

        data_manager.update_file(data_manager.LIST_OF_QUESTIONS)

        if url_origin == "index":
            return redirect(url_for("index"))
        elif url_origin == "display_question":
            return redirect(url_for("display_a_question", question_id = question_id))
    else: # vote_for_answer
        answer_id = request.form.get("answer_id")
        answer = data_manager.find_by_id(answer_id, data_manager.LIST_OF_ANSWERS, mode="for_answer")
        answer_index = data_manager.LIST_OF_ANSWERS.index(answer[0])

        if vote_type == "up_vote":
            data_manager.LIST_OF_ANSWERS[answer_index]["Vote Number"] = int(data_manager.LIST_OF_ANSWERS[answer_index]["Vote Number"]) + 1
        else:
            data_manager.LIST_OF_ANSWERS[answer_index]["Vote Number"] = int(data_manager.LIST_OF_ANSWERS[answer_index]["Vote Number"]) + 1

        data_manager.update_file(data_manager.LIST_OF_ANSWERS, file_type="answer")

        if url_origin == "index":
            return redirect(url_for("index"))
        elif url_origin == "display_question":
            return redirect(url_for("display_a_question", question_id = question_id))

@app.route("/change-question-status", methods=["POST"])
def change_question_status():
    new_question_status = request.form.get("new_question_status")
    question_id = request.form.get("question_id")
    question = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    question_index = data_manager.LIST_OF_QUESTIONS.index(question)
    if new_question_status == "close":
        data_manager.LIST_OF_QUESTIONS[question_index]["Status"] = "closed"
    elif new_question_status == "new":
        data_manager.LIST_OF_QUESTIONS[question_index]["Status"] = "new"
    data_manager.update_file(data_manager.LIST_OF_QUESTIONS)
    return redirect(url_for("index"))

@app.route("/question/<question_id>")
def display_a_question(question_id):
    question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comments_by_question_id(question_id)

    question_tags = [util.take_out_of_the_list(data_manager.get_tag_by_id(tag["tag_id"]))
                     for tag in data_manager.get_question_tags_by_question_id(question_id)]

    return render_template("display_question.html", question=question, answers=answers, comments=comments,
                           question_tags=question_tags, img_path=util.IMAGE_PATH) #img_path=connection.IMAGE_PATH)

    # question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    # relevant_answers_dicts = data_manager.find_by_id(question_id, data_manager.LIST_OF_ANSWERS)
    # relevant_answers_dicts = data_manager.sort_answers(relevant_answers_dicts)
    # question_dict["View Number"] = int(question_dict.get("View Number")) + 1
    # data_manager.update_file(data_manager.LIST_OF_QUESTIONS)
    # return render_template("display_question.html", question=question_dict, answers=relevant_answers_dicts,
    #                        img_path=connection.IMAGE_PATH)

@app.route("/add-question", methods=["GET"])
def add_question_get():
    return render_template("add-question.html", tags_list=data_manager.LIST_OF_TAGS)

# funkcja przerobiona - ale przekierowanie na stronę główną, będę musiała to poprawić na przekierowanie na to nowo dodane pytanie
@app.route("/add-question", methods=["POST"])
def add_question_post():
    question = dict(request.form)
    question["submission_time"] = util.current_datetime()
    data_manager.add_question(question)
    return redirect(url_for("index"))
    # question["submission_time"] = util.todays_date()
    # question["view_number"] = 0
    # question["vote_number"] = 0

    # data_from_form = dict(request.form)
    # tags_list = data_manager.get_tags_list(data_from_form)
    # new_question = {
    #     "Id": str(data_manager.next_id(data_manager.LIST_OF_QUESTIONS)),
    #     "Submission Time": util.todays_date(),
    #     "View Number": "0",
    #     "Vote Number": "0",
    #     "Title": data_from_form["Title"],
    #     "Message": data_from_form["Message"],
    #     "Image": request.files["Image"].filename,
    #     "Tag": tags_list,
    #     "Status": "new"
    # }
    #
    # if new_question["Image"] != '':
    #     image_file = request.files["Image"]
    #     data_manager.add_image(image_file)
    #
    # connection.convert_timestamp_to_date_format([new_question])
    # data_manager.LIST_OF_QUESTIONS.append(new_question)
    # data_manager.update_file(data_manager.LIST_OF_QUESTIONS)
    #
    # return redirect(url_for("display_a_question", question_id=new_question["Id"]))

@app.route("/question/<question_id>/new_answer", methods=["GET"])
def post_an_answer_get(question_id):
    question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
    return render_template("add-question.html", question_id=question_id, question=question)

    # question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    # return render_template("add-question.html", question_id=question_id, question=question_dict,
    #                        tags_list=data_manager.LIST_OF_TAGS)

@app.route("/question/<question_id>/new_answer", methods=["POST"])
def post_an_answer_post(question_id):
    new_answer = dict(request.form)
    new_answer["submission_time"] = util.current_datetime()
    new_answer["image"] = request.files["image"].filename

    if "image" in request.files and request.files["image"].filename != '':
        image_file = request.files["image"]
        util.add_image(image_file)

    data_manager.add_answer(new_answer)
    return redirect(url_for("display_a_question", question_id=question_id))

    # tags_list = data_manager.get_tags_list(data_from_form)
    # new_answer = {
    #     "Id": str(data_manager.next_id(data_manager.LIST_OF_ANSWERS)),
    #     "Submission Time": util.todays_date(),
    #     "Vote Number": "0",
    #     "Question Id": data_from_form["Question Id"],
    #     "Message": data_from_form["Message"],
    #     "Image": request.files["Image"].filename,
    #     "Tag": tags_list
    # }

    # data_manager.update_answer_list(new_answer)
    # return redirect(url_for("display_a_question", question_id=question_id))

@app.route("/answer/<answer_id>/delete endpoint")
def delete_answer(answer_id):
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    question_id = answer["question_id"]
    util.delete_image(answer["image"])
    data_manager.delete_answer(answer_id)
    return redirect(url_for("display_a_question", question_id=question_id))


    # list_of_dicts = data_manager.LIST_OF_ANSWERS
    # answer_to_remove = data_manager.find_by_id(answer_id, list_of_dicts, "for_answer")[0]
    # question_id = answer_to_remove["Question Id"]
    # data_manager.delete_dict(list_of_dicts, answer_to_remove)

    # return redirect(url_for("display_a_question", question_id=question_id))

@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    answers_to_remove = data_manager.find_by_id(question_id, data_manager.LIST_OF_ANSWERS)
    question_to_remove = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)
    if len(answers_to_remove) != 0:
        for answer in answers_to_remove:
            data_manager.delete_dict(data_manager.LIST_OF_ANSWERS, answer)
    data_manager.delete_dict(data_manager.LIST_OF_QUESTIONS, question_to_remove[0])

    return redirect(url_for("index"))

@app.route("/question/<question_id>/edit", methods=["GET"])
def edit_question_get(question_id):
    question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)
    return render_template("edit.html", question_id=question_id, question=question_dict[0], tags_list=data_manager.LIST_OF_TAGS)

@app.route("/question/<question_id>/edit", methods=["POST"])
def edit_question_post(question_id):
    data_from_form = dict(request.form)
    tags_list = data_manager.get_tags_list(data_from_form)
    question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)
    question_to_edit = question_dict[0]
    question_to_edit["Title"] = data_from_form["Title"]
    question_to_edit["Message"] = data_from_form["Message"]
    question_to_edit["Tag"] = tags_list
    if "Image" in request.files and request.files["Image"].filename != '':
        if question_to_edit["Image"] == "":
            image_file = request.files["Image"]
            data_manager.add_image(image_file)
            question_to_edit["Image"] = image_file.filename
        elif request.files["Image"].filename != question_to_edit["Image"]:
            image_file = request.files["Image"]
            data_manager.add_image(image_file)
            data_manager.remove_image(question_to_edit, "question")
            question_to_edit["Image"] = image_file.filename

    data_manager.update_file(data_manager.LIST_OF_QUESTIONS)

    return redirect(url_for("display_a_question", question_id=question_to_edit["Id"]))

@app.route("/question/<question_id>/remove_image")
def delete_image_from_question(question_id):
    question_dict = data_manager.find_by_id(question_id, data_manager.LIST_OF_QUESTIONS)[0]
    data_manager.remove_image(question_dict, "question")
    return redirect(url_for("display_a_question", question_id=question_dict["Id"]))

@app.route("/<answer_id>/delete-img")
def delete_answer_img(answer_id):
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    util.delete_image(answer["image"])
    data_manager.del_answer_img_from_db(answer["id"])
    return redirect(url_for('display_a_question', question_id=answer['question_id']))

    # answer_dict = data_manager.find_by_id(answer_id, data_manager.LIST_OF_ANSWERS, mode="for_answer")[0]
    # data_manager.remove_image(answer_dict, "answer")
    # return redirect(url_for('display_a_question', question_id=answer_dict['Question Id']))

@app.route("/edit/<answer_id>")
def edit_answer_get(answer_id):
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    img_path = os.path.join(util.IMAGE_PATH, answer["image"])
    return render_template('edit.html', answer_id=answer_id, answer=answer, img_path=img_path)

    # answer_dict = data_manager.find_by_id(answer_id, data_manager.LIST_OF_ANSWERS, mode="for_answer")[0]
    # img_path = os.path.join(connection.IMAGE_PATH, answer_dict["Image"])
    # return render_template('edit.html', answer_id=answer_id, answer=answer_dict, img_path=img_path)

@app.route("/edit/<answer_id>", methods=["POST"])
def edit_answer_post(answer_id):
    data_from_form = dict(request.form)
    current_answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    current_answer["message"] = data_from_form["message"]

    if "image" in request.files and request.files["image"].filename != '':
        util.delete_image(current_answer["image"])
        current_answer["image"] = request.files["image"].filename
        util.add_image(request.files["image"])

    data_manager.update_answer(answer_id, current_answer["message"], current_answer["image"])
    return redirect(url_for('display_a_question', question_id=current_answer['question_id']))

    # current_answer = data_manager.find_by_id(answer_id, data_manager.LIST_OF_ANSWERS, mode="for_answer")[0]
    # new_answer = dict(request.form)
    # current_answer["message"] = new_answer["message"]
    #
    # if "image" in request.files and request.files["image"].filename != '':
    #     data_manager.remove_image(current_answer, "answer")
    #     current_answer["Image"] = request.files["Image"].filename
    #     image_file = request.files["Image"]
    #     data_manager.add_image(image_file)
    #
    # data_manager.update_file(data_manager.LIST_OF_ANSWERS, "answer")
    # return redirect(url_for('display_a_question', question_id=current_answer['Question Id']))

@app.route("/login")
def login_get():
    return render_template("login_register.html", login_or_register="login")

@app.route("/login")
def login_post():
    pass

@app.route("/register")
def register_get():
    return render_template("login_register.html", login_or_register="register")

@app.route("/register")
def register_post():
    pass

@app.route("/login-google", methods=["GET"])
def login_google():
    pass

@app.route("/login-google", methods=["POST"])
def login_google_post():
    return ("<h1>google login</h1>")


from flask import Flask

# app = Flask(__name__)


# @app.route("/")
# def hello():
#     return "Hello World!"


if __name__ == "__main__":
    app.run()
