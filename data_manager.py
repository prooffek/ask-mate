from typing import List, Dict

from psycopg2 import sql
from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor
from settings import *

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

import connection


@connection.connection_handler
def get_tags_names(cursor: RealDictCursor) -> list:
    query = """
            SELECT name
            FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
            SELECT *
            FROM question
            WHERE id = %(question_id)s"""
    param = {"question_id": f"{question_id}"}
    cursor.execute(query, param)
    return cursor.fetchall()

@connection.connection_handler
def get_nonquestion_by_question_id(cursor: RealDictCursor, question_id, table_name: str) -> list:
    if table_name == ANSWER_TABLE_NAME:
        query = f"SELECT * \
                FROM {table_name} \
                WHERE question_id = {question_id} \
                ORDER BY vote_number DESC\
                "
        cursor.execute(query)
        return cursor.fetchall()

    elif table_name == COMMENTS_TABLE_NAME:
        query = f"SELECT * \
                FROM {table_name}\
                WHERE question_id = {question_id} \
                ORDER BY submission_time DESC \
                "
        cursor.execute(query)
        return cursor.fetchall()

    else:
        query = f"SELECT * \
                FROM {table_name}\
                WHERE question_id = {question_id} \
                "
        cursor.execute(query)
        return cursor.fetchall()


@connection.connection_handler
def get_tag_by_id(cursor: RealDictCursor, tag_id: int) -> list:
    query = """
            SELECT name
            FROM tag
            WHERE id = %(tag_id)s"""
    param = {"tag_id": tag_id}
    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor: RealDictCursor, question):
    command = """
            INSERT INTO question(submission_time, view_number, vote_number, title, message, image, status, answers_number) 
            VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s, %(status)s, %(answers_number)s)
            RETURNING id
            """

    param = {"submission_time": question.get("submission_time"),
             "view_number": question.get("view_number"),
             "vote_number": question.get("vote_number"),
             "title": question.get("title"),
             "message": question.get("message"),
             "image": question.get("image"),
             "status": question.get("status"),
             "answers_number": question.get("answers_number")}
    cursor.execute(command, param)
    return cursor.fetchone()


@connection.connection_handler
def delete_question(cursor: RealDictCursor, question_id: int):
    command = """
            DELETE
            FROM question
            WHERE id = %(question_id)s
    """

    param = {"question_id": question_id}
    cursor.execute(command, param)


@connection.connection_handler
def delete_answers_by_question_id(cursor: RealDictCursor, question_id: int):
    command = """
            DELETE
            FROM answer
            WHERE question_id = %(question_id)s
    """
    param = {"question_id": question_id}

    cursor.execute(command, param)

@connection.connection_handler
def get_headers_from_table(cursor: RealDictCursor, table_name) -> list:
    query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %(table_name)s
            """
    param = {"table_name": table_name}
    cursor.execute(query, param)
    headers = cursor.fetchall()

    # set proper columns order for listing questions on index.html page
    column = {question.vote_number:3, question.view_number:2, question.answers_number:8, question.title:4, question.status:7, question.submission_time:1, question.id:0, question.message:5, question.image:6}
    new_headers = [\
            headers[column[question.vote_number]],\
                      headers[column[question.view_number]],\
                      headers[column[question.answers_number]],\
                      headers[column[question.title]],\
                      headers[column[question.status]],\
                      headers[column[question.submission_time]],\
                      headers[column[question.id]],\
                      headers[column[question.message]],\
                      headers[column[question.image]]\
                      ]
    return new_headers

@connection.connection_handler
def get_list_questions(cursor: RealDictCursor, actual_filters:list, sorting_mode:list) -> list:

    actual_filter_by_date_mode = actual_filters[0]
    actual_filter_by_status_mode = actual_filters[1]
    actual_filter_by_search_mode = actual_filters[2]

    query_part_by_date = ""
    if actual_filter_by_date_mode == filter.date_last_month:
        query_part_by_date = (datetime.now() + relativedelta(months=-1)).strftime("%Y-%m-%d")
    elif actual_filter_by_date_mode == filter.date_3_last_months:
        query_part_by_date = (datetime.now() + relativedelta(months=-3)).strftime("%Y-%m-%d")
    elif actual_filter_by_date_mode == filter.date_all_time:
        query_part_by_date = filter.date_starting_point_for_all_time_question

    query_part_by_status = ""
    if actual_filter_by_status_mode == filter.status_new:
        query_part_by_status = "status = 'new'"
    elif actual_filter_by_status_mode == filter.status_discussed:
        query_part_by_status = "status = 'discussed'"
    elif actual_filter_by_status_mode == filter.status_active:
        query_part_by_status = "status IN ('new', 'discussed')"
    elif actual_filter_by_status_mode == filter.status_closed:
        query_part_by_status = "status = 'closed'"
    elif actual_filter_by_status_mode == filter.status_all:
        query_part_by_status = "status IN ('new', 'discussed', 'closed')"


    sorting_column = sorting_mode[0]
    sorting_direction = "DESC" if sorting_mode[1] == sort.descending else "ASC"

    full_query = f" \
            SELECT vote_number, view_number, answers_number, title, status, submission_time, id, message, image \
            FROM question \
            WHERE  submission_time >= '{query_part_by_date}' \
            AND {query_part_by_status} \
            AND (title LIKE '%%{actual_filter_by_search_mode}%%'\
                OR message LIKE '%%{actual_filter_by_search_mode}%%' \
            )\
            ORDER BY {sorting_column} {sorting_direction}\
    "

    param = {
        "sorting_column" : sorting_column,
        "sorting_direction" : f"{sorting_direction}"
    }
    cursor.execute(full_query, param)
    questions = cursor.fetchall()
    return questions


# @connection.connection_handler
# def get_id(cursor: RealDictCursor, name_table):
#     query = """
#         SELECT CURRVAL(pg_get_serial_sequence('sheet_tbl','sheet_id'))";
#     """

@connection.connection_handler
def get_answer_by_answer_id(cursor: RealDictCursor, answer_id: int) -> dict:
    query = """
            SELECT *
            FROM answer
            WHERE id = %(answer_id)s"""
    param = {"answer_id": f"{answer_id}"}
    cursor.execute(query, param)
    return cursor.fetchall()

@connection.connection_handler
def vote_for_question(cursor: RealDictCursor, question_id: int, vote_up_or_down="up") -> None:
    operant = '+' if vote_up_or_down == "up" else '-'
    query = f"UPDATE question \
    SET vote_number = vote_number {operant} 1 \
    WHERE id = {question_id}"
    cursor.execute(query)

@connection.connection_handler
def vote_for_answer(cursor: RealDictCursor, answer_id: int, vote_up_or_down="up") -> None:
    operant = '+' if vote_up_or_down == "up" else '-'
    query = f"UPDATE answer \
    SET vote_number = vote_number {operant} 1 \
    WHERE id = {answer_id}"
    cursor.execute(query)

@connection.connection_handler
def add_answer(cursor: RealDictCursor, answer: dict):
    command = """
            INSERT INTO answer(submission_time, vote_number, question_id, message, image)
            VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s)"""
    param = {
            "submission_time": answer["submission_time"],
            "vote_number": answer["vote_number"],
            "question_id": answer["question_id"],
            "message": answer["message"],
            "image": answer["image"]
            }
    cursor.execute(command, param)


@connection.connection_handler
def get_answer_image(cursor: RealDictCursor, answer_id) -> list:
    query = """
            SELECT image
            FROM answer
            WHERE id = %(answer_id)s"""
    param = {"answer_id": f"{answer_id}"}
    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def update_answer(cursor: RealDictCursor, answer_id, new_message: str, new_image: str):
    command = """
            UPDATE answer
            SET message = %(new_message)s,
                image = %(new_image)s
            WHERE id = %(answer_id)s"""
    param = {
        "new_message": f"{new_message}",
        "new_image": f"{new_image}",
        "answer_id": f"{answer_id}"
    }
    cursor.execute(command, param)


@connection.connection_handler
def del_answer_img_from_db(cursor: RealDictCursor, answer_id):
    command = """
            UPDATE answer 
            SET image = %(image)s
            WHERE id = %(answer_id)s"""
    param = {"image": "",
             "answer_id": f"{answer_id}"}
    cursor.execute(command, param)


@connection.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id):
    command = """
            DELETE FROM answer
            WHERE id = %(answer_id)s"""
    param = {"answer_id": f"{answer_id}"}
    cursor.execute(command, param)

@connection.connection_handler
def update_question(cursor: RealDictCursor, question, question_id):
    command = """
           UPDATE question
           SET title = %(title)s,
               message = %(message)s,
               image = %(image)s, 
               view_number = %(view_number)s,
               status = %(status)s,
               answers_number = %(answers_number)s
           WHERE id = %(question_id)s       
    """
    param = {"title": question["title"],
             "message": question["message"],
             "image": question["image"],
             "view_number": question["view_number"],
             "status": question["status"],
             "answers_number": question["answers_number"],
             "question_id": question_id
             }
    cursor.execute(command, param)


@connection.connection_handler
def add_comment_to_question(cursor: RealDictCursor, comment):
    command = """
            INSERT INTO comment(question_id, message, submission_time)
            VALUES (%(question_id)s, %(message)s, %(submission_time)s)
    """

    param = {
        "question_id": comment["question_id"],
        "message": comment["message"],
        "submission_time": comment["submission_time"],

            }
    cursor.execute(command, param)


@connection.connection_handler
def add_comment_to_answer(cursor: RealDictCursor, comment: dict):
    query = """
            INSERT INTO comment(answer_id, message, submission_time, edited_count)
            VALUES (%(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)"""
    param = {
        "answer_id": f"{comment['answer_id']}",
        "message": f"{comment['message']}",
        "submission_time": f"{comment['submission_time']}",
        "edited_count": f"{comment['edited_count']}"
    }
    cursor.execute(query, param)


@connection.connection_handler
def get_all_comments(cursor: RealDictCursor) -> RealDictCursor:
    query = """
            SELECT *
            FROM comment"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_comment_by_comment_id(cursor: RealDictCursor, comment_id):
    query = """
        SELECT *
        FROM comment
        WHERE id = %(comment_id)s
    """
    param = {
        "comment_id": comment_id
    }

    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def update_comment(cursor: RealDictCursor, comment):
    command = """
               UPDATE comment
               SET message = %(message)s,
                   submission_time = %(submission_time)s,
                   edited_count = %(edited_count)s 
               WHERE id = %(comment_id)s       
        """
    param = {"message": comment["message"],
             "submission_time": comment["submission_time"],
             "edited_count": comment["edited_count"],
             "comment_id": comment["id"]
             }
    cursor.execute(command, param)


@connection.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id):
    command = """
                DELETE FROM comment
                WHERE id = %(comment_id)s"""
    param = {"comment_id": f"{comment_id}"}
    cursor.execute(command, param)


@connection.connection_handler
def get_tags_with_ids(cursor: RealDictCursor) -> list:
    query = """
            SELECT *
            FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_tag(cursor: RealDictCursor, tag_name: str):
    command = """
            INSERT INTO tag("name")
            VALUES (%(tag_name)s)"""
    param = {"tag_name": f"{tag_name}"}
    cursor.execute(command, param)

@connection.connection_handler
def add_question_tag(cursor: RealDictCursor, question_id, tag_id):
    command = """
                INSERT INTO question_tag(question_id, tag_id)
                VALUES (%(question_id)s, %(tag_id)s)"""
    param = {
            "question_id": f"{question_id}",
            "tag_id": f"{tag_id}"
    }
    cursor.execute(command, param)


@connection.connection_handler
def del_question_tag(cursor: RealDictCursor, question_id):
    command = f"""
            DELETE
            FROM question_tag
            WHERE question_id = %(question_id)s"""
    param = {"question_id": f"{question_id}"}
    cursor.execute(command, param)