QUESTION_TABLE_NAME = "question"
ANSWER_TABLE_NAME = "answer"
COMMENTS_TABLE_NAME = "comment"
QUESTION_TAG_TABLE_NAME = "question_tag"


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

class sort:
    ascending = "ascending"
    descending = "descinding"

class filter:
    date_last_month = "Last month"
    date_3_last_months = "3 last months"
    date_all_time = "all time"

    status_new = "new"
    status_discussed = "discussed"
    status_active = "active"
    status_closed = "closed"

    search = ""

class state:
    on = "yes"
    off = "no"
