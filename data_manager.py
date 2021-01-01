import connection
from connection import csv_question_headers, csv_answer_headers

questions_default_filename = "question.csv"
answers_default_filename = "answer.csv"

LIST_OF_QUESTIONS = connection.read_from_file(questions_default_filename)
LIST_OF_QUESTIONS = connection.convert_timestamp_to_date_format(LIST_OF_QUESTIONS)
LIST_OF_ANSWERS = connection.convert_timestamp_to_date_format(connection.read_from_file(answers_default_filename))

titles_for_questions_columns = {
    csv_question_headers.id:'Id',
    csv_question_headers.submission_time:'Submission Time',
    csv_question_headers.view_number:'View Number',
    csv_question_headers.vote_number:'Vote Number',
    csv_question_headers.title:'Title',
    csv_question_headers.message:'Message',
    csv_question_headers.image:'Image',
}


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

    # for dictionary in list_of_dicts:
    #     if ((mode == "for_question" and ((list_of_dicts == LIST_OF_QUESTIONS and dictionary["Id"] == id_to_find) or
    #              (list_of_dicts == LIST_OF_ANSWERS and dictionary["Question Id"] == id_to_find))) or
    #         (mode == "for_answer" and dictionary["Id"] == id_to_find)):
    #         list_to_return.append(dictionary)

    return list_to_return

def find_answers_number_for_questions(LIST_OF_QUESTIONS: list, LIST_OF_ANSWERS: list) -> dict:
    # function returns dict question_id:number_of_answers
    answers_number_for_questions = {}
    for question in LIST_OF_QUESTIONS:
        current_answers_number = len(find_by_id(question[csv_question_headers.id], LIST_OF_ANSWERS, "for_question"))
        answers_number_for_questions[str(question[csv_question_headers.id])] = current_answers_number
    return answers_number_for_questions




# def navigate_by_id(question_id):
#     return [str(int(question_id) - 1), str(int(question_id) + 1)]


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
    except:
        ValueError("Problems while trying update questions, save to file")


def next_id(list_of_dicts):
    try:
        return max(int(dictionary["Id"]) for dictionary in list_of_dicts) + 1
    except:
        ValueError

def update_answer_list(new_answer):
    connection.append_to_file("answer.csv", new_answer)
    new_answer = connection.convert_timestamp_to_date_format([new_answer])
    LIST_OF_ANSWERS.append(new_answer[0])


def delete_dict(list_of_dicts, dict_to_remove):
    if list_of_dicts == LIST_OF_QUESTIONS:
        list_of_dicts.remove(dict_to_remove)
        update_file(list_of_dicts)
    elif list_of_dicts == LIST_OF_ANSWERS:
        list_of_dicts.remove(dict_to_remove)
        connection.write_to_file("answer.csv", list_of_dicts)


