import connection

LIST_OF_QUESTIONS = connection.read_from_file("question.csv")
LIST_OF_ANSWERS = connection.read_from_file("answer.csv")

# keys for question table (from question.csv)
id = 'id'
submission_time = 'submission_time'
view_number = 'view_number'
vote_number = 'vote_number'
title = 'title'
message = 'message'
image = 'image'

def find_by_id(id_to_find, list_of_dicts):
    list_to_return = []

    for dictionary in list_of_dicts:
        if ((list_of_dicts == LIST_OF_QUESTIONS and dictionary["id"] == id_to_find) or
            (list_of_dicts == LIST_OF_ANSWERS and dictionary["question_id"] == id_to_find)):
            list_to_return.append(dictionary)
    return list_to_return


# mode = 'ascending' or 'descending'
# for question table columns:

def sort_question(list_of_dicts: list, sort_column, mode='ascending') -> list:

    correct_sort_column = [
        id,
        submission_time,
        view_number,
        vote_number,
        title,
        message,
        ]
    if not (sort_column in correct_sort_column and mode in ['ascending', 'descending']):
        return list_of_dicts


    if sort_column in [id, submission_time, view_number, vote_number]:
        sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: int(row[sort_column]))
    else:
        sorted_list_of_dicts = sorted(list_of_dicts, key=lambda row: row[sort_column])

    if mode == 'descending':
        sorted_list_of_dicts = sorted_list_of_dicts[::-1]

    return sorted_list_of_dicts
