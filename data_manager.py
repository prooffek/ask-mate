import connection
from connection import csv_question_headers

LIST_OF_QUESTIONS = connection.read_from_file("question.csv")
LIST_OF_QUESTIONS = connection.convert_timestamp_to_date_format(LIST_OF_QUESTIONS)
LIST_OF_ANSWERS = connection.read_from_file("answer.csv")

titles_for_questions_columns = {
    csv_question_headers.id:'ID',
    csv_question_headers.submission_time:'Time',
    csv_question_headers.view_number:'Views',
    csv_question_headers.vote_number:'Votes',
    csv_question_headers.title:'Title',
    csv_question_headers.message:'Message',
    csv_question_headers.image:'Image',
}

def find_by_id(id_to_find, list_of_dicts):
    list_to_return = []

    for dictionary in list_of_dicts:
        if ((list_of_dicts == LIST_OF_QUESTIONS and dictionary["id"] == id_to_find) or
            (list_of_dicts == LIST_OF_ANSWERS and dictionary["question_id"] == id_to_find)):
            list_to_return.append(dictionary)
    return list_to_return


def sort_question(list_of_dicts: list, sort_column, mode='ascending') -> list:

    correct_sort_column = titles_for_questions_columns.keys()
    if not (sort_column in correct_sort_column and mode in ['ascending', 'descending']):
        return list_of_dicts


    if sort_column in [id, submission_time, view_number, vote_number]:
        sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: int(row[sort_column]))
    else:
        sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: row[sort_column])

    if mode == 'descending':
        sorted_list_of_dicts = sorted_list_of_dicts[::-1]

    return sorted_list_of_dicts
