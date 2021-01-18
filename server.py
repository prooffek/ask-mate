from flask import Flask, render_template, url_for, redirect, request
import data_manager, util, connection, os
import copy

app = Flask(__name__)

LIST_OF_TAGS = data_manager.get_tags_names()
QUESTION_TABLE_NAME = "question"
ANSWER_TABLE_NAME = "answer"
COMMENTS_TABLE_NAME = "comment"
QUESTION_TAG_TABLE_NAME = "question_tag"

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
    headers = data_manager.get_headers_from_table("question")
    questions = data_manager.get_list_questions()

    return render_template("index.html", headers=headers, questions=questions, server_state=server_state)


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
    answers = data_manager.get_nonquestion_by_question_id(question_id, ANSWER_TABLE_NAME)
    comments = data_manager.get_all_comments()
    tags = data_manager.get_nonquestion_by_question_id(question_id, QUESTION_TAG_TABLE_NAME)

    question_tags = [util.take_out_of_the_list(data_manager.get_tag_by_id(tag["tag_id"]))
                     for tag in tags]

    return render_template("display_question.html", question=question, answers=answers, comments=comments,
                           question_tags=question_tags, img_path=util.IMAGE_PATH) #img_path=connection.IMAGE_PATH)


@app.route("/add-question", methods=["GET"])
def add_question_get():
    return render_template("add-question.html")


# funkcja przerobiona - ale przekierowanie na stronę główną, będę musiała to poprawić na przekierowanie na to nowo dodane pytanie
@app.route("/add-question", methods=["POST"])
def add_question_post():
    question = dict(request.form)
    question["submission_time"] = util.current_datetime()
    file_name = request.files["image"].filename
    if file_name != "":
        image_file = request.files["image"]
        util.add_image(image_file)
        question["image"] = image_file.filename
    return_value = data_manager.add_question(question)

    return redirect(url_for("display_a_question", question_id=return_value["id"]))


@app.route("/question/<question_id>/new_answer", methods=["GET"])
def post_an_answer_get(question_id):
    question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
    return render_template("add-question.html", question_id=question_id, question=question)


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


@app.route("/answer/<answer_id>/delete endpoint")
def delete_answer(answer_id):
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    question_id = answer["question_id"]
    util.delete_image(answer["image"])
    data_manager.delete_answer(answer_id)
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    data_manager.delete_answers_by_question_id(question_id)
    return redirect(url_for("index"))


@app.route("/question/<question_id>/edit", methods=["GET"])
def edit_question_get(question_id):
    question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
    return render_template("edit.html", question_id=question_id, question=question)

@app.route("/question/<question_id>/edit", methods=["POST"])
def edit_question_post(question_id):
    data_from_form = dict(request.form)
    question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
    if "image" in request.files and request.files["image"].filename != '':
        if question["image"] == "":
            image_file = request.files["image"]
            util.add_image(image_file)
            question["image"] = image_file.filename
        elif request.files["image"].filename != question["image"]:
            image_file = request.files["image"]
            util.add_image(image_file)
            util.delete_image(question["image"])
            question["image"] = image_file.filename

    question["title"] = data_from_form["title"]
    question["message"] = data_from_form["message"]
    data_manager.update_question(question, question["id"])
    return redirect(url_for("display_a_question", question_id=question["id"]))


@app.route("/question/<question_id>/remove_image")
def delete_image_from_question(question_id):
    question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
    util.delete_image(question["image"])
    question["image"] = ""
    data_manager.update_question(question, question_id)
    return redirect(url_for("display_a_question", question_id=question_id))

@app.route("/<answer_id>/delete-img")
def delete_answer_img(answer_id):
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    util.delete_image(answer["image"])
    data_manager.del_answer_img_from_db(answer["id"])
    return redirect(url_for('display_a_question', question_id=answer['question_id']))

@app.route("/edit/<answer_id>")
def edit_answer_get(answer_id):
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    img_path = os.path.join(util.IMAGE_PATH, answer["image"])
    return render_template('edit.html', answer_id=answer_id, answer=answer, img_path=img_path)

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

@app.route("/question/<question_id>/new-comment", methods=["GET"])
def add_comment_to_question_get(question_id):
    question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
    return render_template("add-comment.html", question=question, mode="question")

@app.route("/question/<question_id>/new-comment", methods=["POST"])
def add_comment_to_question_post(question_id):
    comment = dict(request.form)
    comment["submission_time"] = util.current_datetime()
    data_manager.add_comment_to_question(comment)
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/answer/<answer_id>/new-comment')
def add_comment_to_answer_get(answer_id):
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    question = util.take_out_of_the_list(data_manager.get_question_by_id(answer["question_id"]))
    return render_template("add-comment.html", answer=answer, question=question, mode="answer")


@app.route('/answer/<answer_id>/new-comment', methods=["POST"])
def add_comment_to_answer_post(answer_id):
    comment = dict(request.form)
    comment["submission_time"] = util.current_datetime()
    data_manager.add_comment_to_answer(comment)
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    return redirect(url_for("display_a_question", question_id=answer["question_id"]))


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


if __name__ == "__main__":
    app.run()
