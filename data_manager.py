from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import connection

from connection import csv_question_headers, csv_answer_headers
from data_manager_filter import Questions_status

questions_default_filename = "question_long_list.csv"
answers_default_filename = "answer_short_list.csv"
tags_default_filename = "tag.csv"

LIST_OF_QUESTIONS = connection.convert_timestamp_to_date_format(connection.read_from_file(questions_default_filename))
LIST_OF_QUESTIONS = connection.str_to_list(LIST_OF_QUESTIONS)

LIST_OF_ANSWERS = connection.convert_timestamp_to_date_format(connection.read_from_file(answers_default_filename))
LIST_OF_ANSWERS = connection.str_to_list(LIST_OF_ANSWERS)

LIST_OF_TAGS = connection.read_from_file(tags_default_filename)

titles_for_questions_columns = {
    csv_question_headers.id: 'Id',
    csv_question_headers.submission_time: 'Submission Time',
    csv_question_headers.view_number: 'View Number',
    csv_question_headers.vote_number: 'Vote Number',
    csv_question_headers.title: 'Title',
    csv_question_headers.message: 'Message',
    csv_question_headers.image: 'Image',
    csv_question_headers.status: 'Status'
}


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
def get_answers_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
                SELECT *
                FROM answer
                WHERE question_id = %(question_id)s"""
    param = {"question_id": f"{question_id}"}
    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def get_comments_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
                SELECT *
                FROM comment
                WHERE question_id = %(question_id)s"""
    param = {"question_id": f"{question_id}"}
    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def get_question_tags_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
                SELECT *
                FROM question_tag
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
            """

    param = {"submission_time": question.get("submission_time"),
             "view_number": question.get("view_number"),
             "vote_number": question.get("vote_number"),
             "title": question.get("title"),
             "message": question.get("message"),
             "image": question.get("image")}
    cursor.execute(command, param)


@connection.connection_handler
def delete_question(cursor: RealDictCursor, question_id: int):
    command = """
            DELETE
            FROM question
            WHERE id = %(question_id)s
    """

    param = {"id": question_id}
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
def get_headers_from_table(cursor:RealDictCursor, table_name) -> list:
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
            ORDER BY submission_time
    """
    cursor.execute(query)
    return cursor.fetchall()


# @connection.connection_handler
# def get_id(cursor: RealDictCursor, name_table):
#     query = """
#         SELECT CURRVAL(pg_get_serial_sequence('sheet_tbl','sheet_id'))";
#     """

"""
_______________________________________________
            OLD DATA MANAGER
_______________________________________________
"""

def find_by_id(id_to_find, list_of_dicts, mode="for_question"):
    list_to_return = []

    """To make this function more universal, two modes have been applied:
        mode_1: looks for questions and answers based on the question_id - necessary to link answers with proper questions
        mode 2: looks for answers based on the answer_id - necessary to delete answer without affecting other data"""

    for dictionary in list_of_dicts:
        mode_1 = (mode == "for_question" and
                          ((list_of_dicts == LIST_OF_QUESTIONS and dictionary["Id"] == id_to_find) or
                           (list_of_dicts == LIST_OF_ANSWERS and dictionary["Question Id"] == id_to_find)))
        mode_2 = (mode == "for_answer" and dictionary["Id"] == id_to_find)

        if mode_1 or mode_2:
            list_to_return.append(dictionary)

    return list_to_return

def find_answers_number_for_questions(LIST_OF_QUESTIONS: list, LIST_OF_ANSWERS: list) -> dict:
    answers_number_for_questions = {}
    for question in LIST_OF_QUESTIONS:
        current_answers_number = len(find_by_id(question[csv_question_headers.id], LIST_OF_ANSWERS, "for_question"))
        answers_number_for_questions[str(question[csv_question_headers.id])] = current_answers_number
    return answers_number_for_questions

def update_questions_statuses(LIST_OF_QUESTIONS: list, LIST_OF_ANSWERS: list):
    for question in LIST_OF_QUESTIONS:
        current_answers_number = len(find_by_id(question[csv_question_headers.id], LIST_OF_ANSWERS, "for_question"))
        if question[csv_question_headers.status] == Questions_status["closed"]:
            question[csv_question_headers.status] = Questions_status["closed"]
        elif current_answers_number > 0:
            question[csv_question_headers.status] = Questions_status["discussed"]
        else:
            question[csv_question_headers.status] = Questions_status["new"]

def sort_question(list_of_dicts: list, sort_column, mode='ascending') -> list:

    correct_sort_column = titles_for_questions_columns.keys()
    if not (sort_column in correct_sort_column and mode in ['ascending', 'descending']):
        return list_of_dicts

    if sort_column in [csv_question_headers.id, csv_question_headers.view_number, csv_question_headers.vote_number]:
        sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: int(row[sort_column]))
        sorted_list_of_dicts = sorted_list_of_dicts[::-1]
    elif sort_column == csv_question_headers.submission_time:
        sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: (row[sort_column]))
        sorted_list_of_dicts = sorted_list_of_dicts[::-1]
    else:
        sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: row[sort_column])

    if mode == 'descending':
        sorted_list_of_dicts = sorted_list_of_dicts[::-1]

    return sorted_list_of_dicts

def sort_question_by_answers_number(list_of_dicts: list, answers_number_for_question: dict, mode='ascending') -> list:
    sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: answers_number_for_question[row[csv_question_headers.id]])
    if mode == 'descending':
        sorted_list_of_dicts = sorted_list_of_dicts[::-1]
    return sorted_list_of_dicts

def sort_answers(list_of_dicts: list, sort_column = csv_answer_headers.vote_number, mode='ascending') -> list:
    sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: int(row[csv_answer_headers.vote_number]))
    return sorted_list_of_dicts[::-1]

def update_file(NEW_LIST: list, file_type="question"):
    try:
        if file_type == "question":
            filename = questions_default_filename
        elif file_type == "answer":
            filename = answers_default_filename
        connection.write_to_file(filename, NEW_LIST)
    except ValueError:
        ValueError("Problems while trying update questions, save to file")

def next_id(list_of_dicts):
    return max(int(dictionary["Id"]) for dictionary in list_of_dicts) + 1

def update_answer_list(new_answer):
    connection.append_to_file(answers_default_filename, [new_answer])
    new_answer = connection.convert_timestamp_to_date_format([new_answer])
    new_answer = connection.str_to_list(new_answer)
    LIST_OF_ANSWERS.append(new_answer[0])

def delete_dict(list_of_dicts, dict_to_remove):
    if list_of_dicts == LIST_OF_QUESTIONS:
        list_of_dicts.remove(dict_to_remove)
        update_file(list_of_dicts)

    elif list_of_dicts == LIST_OF_ANSWERS:
        list_of_dicts.remove(dict_to_remove)
        connection.write_to_file(answers_default_filename, list_of_dicts)

def add_image(image_file):
    connection.image_to_file(image_file)

def remove_image(dict_to_edit, mode):
    connection.delete_image(dict_to_edit["Image"])
    dict_to_edit["Image"] = ""
    if mode == "question":
        update_file(LIST_OF_QUESTIONS)
    else:
        update_file(LIST_OF_ANSWERS, "answer")

def get_tags_list(dictionary):
    names_list = [dictionary["Name"] for dictionary in LIST_OF_TAGS]
    return [value for key, value in dictionary.items() if key in names_list]
