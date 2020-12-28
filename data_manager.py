import connection
from connection import csv_question_headers

LIST_OF_QUESTIONS = connection.read_from_file("question.csv")
LIST_OF_QUESTIONS = connection.convert_timestamp_to_date_format(LIST_OF_QUESTIONS)
LIST_OF_ANSWERS = connection.convert_timestamp_to_date_format(connection.read_from_file("answer.csv"))

titles_for_questions_columns = {
    csv_question_headers.id:'Id',
    csv_question_headers.submission_time:'Submission Time',
    csv_question_headers.view_number:'View Number',
    csv_question_headers.vote_number:'Vote Number',
    csv_question_headers.title:'Title',
    csv_question_headers.message:'Message',
    csv_question_headers.image:'Image',
}

def find_by_id(id_to_find, list_of_dicts):
    list_to_return = []

    for dictionary in list_of_dicts:
        if ((list_of_dicts == LIST_OF_QUESTIONS and dictionary["Id"] == id_to_find) or
            (list_of_dicts == LIST_OF_ANSWERS and dictionary["Question Id"] == id_to_find)):
            list_to_return.append(dictionary)
    return list_to_return


def navigate_by_id(question_id):
    return [str(int(question_id) - 1), str(int(question_id) + 1)]


def sort_question(list_of_dicts: list, sort_column, mode='ascending') -> list:

    correct_sort_column = titles_for_questions_columns.keys()
    if not (sort_column in correct_sort_column and mode in ['ascending', 'descending']):
        return list_of_dicts


    if sort_column in [csv_question_headers.id, csv_question_headers.view_number, csv_question_headers.vote_number]:
        sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: int(row[sort_column]))
    else:
        sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: row[sort_column])

    if mode == 'descending':
        sorted_list_of_dicts = sorted_list_of_dicts[::-1]

    return sorted_list_of_dicts
