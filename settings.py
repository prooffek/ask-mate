QUESTION_TABLE_NAME = "question"
ANSWER_TABLE_NAME = "answer"
COMMENTS_TABLE_NAME = "comment"
QUESTION_TAG_TABLE_NAME = "question_tag"
FORM_USERNAME = "user_name"
FORM_PASSWORD = "password"
FORM_CONFIRM_PSWRD = "confirm_password"
FORM_EMAIL = "email"
FORM_USER_PHOTO = "user_photo"
DB_USER_ID = "user_id"
SESSION_KEY = DB_USER_ID


class answer:
    id = "id"
    submission_time = "submission_time"
    vote_number = "vote_number"
    question_id = "question_id"
    message = "message"
    image = "image"


class question:
    id = "id"
    submission_time = "submission_time"
    view_number = "view_number"
    vote_number = "vote_number"
    title = "title"
    message = "message"
    image = "image"
    status = "status"
    answers_number = "answers_number"

class comments:
    id = "id"
    question_id = "question_id"
    answer_id = "answer_id"
    message = "message"
    submission_time = "submission_time"
    edited_count = "edited_count"

class question_tag:
    question_id = "question_id"
    tag_id = "tag_id"

class tag:
    id = "id"
    name = "name"

    all_tags = "all_tags"

class sort:
    ascending = "ascending"
    descending = "descending"

class filter:
    date_last_month = "Last month"
    date_3_last_months = "3 last months"
    date_all_time = "All time"
    date_starting_point_for_all_time_question = '0001-01-01'

    status_new = "new"
    status_discussed = "discussed"
    status_active = "active"
    status_closed = "closed"
    status_all = "All status"

    search_empty = ""

class state:
    on = "yes"
    off = "no"

class user_page:
    is_enabled_user_activity_lists_default = "no"
    user_activity_list_default = "answer" # possible states "answer", "question", "comment"

