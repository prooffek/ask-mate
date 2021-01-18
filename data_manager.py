from typing import List, Dict

from psycopg2 import sql
from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor

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
    query = f"""
            SELECT *
            FROM {table_name}
            WHERE question_id = %(question_id)s"""
    param = {"question_id": f"{question_id}"}
    cursor.execute(query, param)
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
            INSERT INTO question(submission_time, view_number, vote_number, title, message, image) 
            VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s)
            RETURNING id
            """

    param = {"submission_time": question.get("submission_time"),
             "view_number": question.get("view_number"),
             "vote_number": question.get("vote_number"),
             "title": question.get("title"),
             "message": question.get("message"),
             "image": question.get("image")}
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
    return cursor.fetchall()

@connection.connection_handler
def get_list_questions(cursor: RealDictCursor) -> list:
    query = """
            SELECT *
            FROM question
            ORDER BY submission_time desc
            LIMIT 5
    """
    cursor.execute(query)
    return cursor.fetchall()


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
               image = %(image)s 
           WHERE id = %(question_id)s       
    """
    param = {"title": question["title"],
             "message": question["message"],
             "image": question["image"],
             "question_id": question_id}
    cursor.execute(command, param)


@connection.connection_handler
def add_comment_to_question(cursor: RealDictCursor, comment):
    command = """
            INSERT INTO comment(question_id, message, submission_time, edited_count)
            VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
    """

    param = {
        "question_id": comment["question_id"],
        "message": comment["message"],
        "submission_time": comment["submission_time"],
        "edited_count": comment["edited_count"]
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

