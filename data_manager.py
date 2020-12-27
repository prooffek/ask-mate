import connection

LIST_OF_QUESTIONS = connection.read_from_file("question.csv")
LIST_OF_ANSWERS = connection.read_from_file("answer.csv")

def find_by_id(id_to_find, list_of_dicts):
    list_to_return = []

    for dictionary in list_of_dicts:
        if ((list_of_dicts == LIST_OF_QUESTIONS and dictionary["id"] == id_to_find) or
            (list_of_dicts == LIST_OF_ANSWERS and dictionary["question_id"] == id_to_find)):
            list_to_return.append(dictionary)
    return list_to_return
