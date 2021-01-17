import os
import psycopg2
import psycopg2.extras


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper







"""
–––––––––––––––––––––––––––––––––––––––––––––––––––
            OLD CONNECTION
–––––––––––––––––––––––––––––––––––––––––––––––––––
"""

import csv, os
from pathlib import Path
from datetime import datetime


path = f"{Path(__name__).parent}/sample_data"
IMAGE_PATH = f"/static/users_images"
IMAGE_FOLDER_PATH = f"{Path(__name__).parent}{IMAGE_PATH}"

class csv_question_headers:
    id = "Id"
    submission_time = "Submission Time"
    view_number = "View Number"
    vote_number = "Vote Number"
    title = "Title"
    message = "Message"
    image = "Image"
    status = "Status"

class csv_answer_headers:
    id = "Id"
    subission_time = "Submission Time"
    vote_number = "Vote Number"
    question_id = "Question Id"
    message = "Message"
    image = "Image"

def read_from_file(filename):
    filename = f"{path}/{filename}"
    data = []
    tmp_data = []
    try:
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                tmp_data.append(row)
    except FileNotFoundError:
        print("File Not Found")

    keys = tmp_data[0]
    for element in tmp_data[1:]:
        tmp_dict = {}
        empty_list = []
        if element != empty_list:
            for i in range(len(keys)):
                tmp_dict[keys[i]] = element[i]
            data.append(tmp_dict)

    return data

def convert_timestamp_to_date_format(table: list) -> list:
    for row in table:
        row[csv_question_headers.submission_time] = datetime.fromtimestamp(int(row[csv_question_headers.submission_time]))
    return table

def convert_date_to_timestamp_format(table: list) -> list:
    new_table = []
    for row in table:
        new_row = row.copy()
        new_row[csv_question_headers.submission_time] = str(int(datetime.timestamp((new_row[csv_question_headers.submission_time]))))
        new_table.append(new_row)
    return new_table

def str_to_list(list_of_dicts, key="Tag", separator=","):
    for dictionary in list_of_dicts:
        dictionary[key] = dictionary[key].split(separator)

    return list_of_dicts

def list_to_str(list_of_dicts, key="Tag", separator=","):
    for dictionary in list_of_dicts:
        if dictionary[key] == [""]:
            dictionary[key] = ""
        else:
            dictionary[key] = separator.join(dictionary[key])

    return list_of_dicts

def append_to_file(filename, dict_to_add):
    filename = f"{path}/{filename}"
    dict_to_add = list_to_str(dict_to_add)[0]

    list_of_values = list(dict_to_add.values())
    try:
        f = open(filename, "a", encoding='utf-8')
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(list_of_values)
        f.close()
        print("The question/answer has been added successfully.")
    except:
        ValueError("An error has occured. Question/Answer has not been added.")

def write_to_file(filename, list_of_dicts_to_save, csv_separator = ','):
    try:
        filename = f"{path}/{filename}"
        list_of_dicts_to_save_new = (convert_date_to_timestamp_format(list_of_dicts_to_save)).copy()
        list_of_dicts_to_save_new = (list_to_str(list_of_dicts_to_save_new))
        with open(filename, mode="w",  newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=csv_separator, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(list_of_dicts_to_save_new[0].keys())
            for record in list_of_dicts_to_save_new:
                row = record.values()
                csv_writer.writerow(row)
    except IOError:
        print(f"IOError while trying to open {filename} to write.")

# def image_to_file(image):
#     image.save(os.path.join(IMAGE_FOLDER_PATH, image.filename))


# def delete_image(filename):
#     path_image = os.path.join(IMAGE_FOLDER_PATH, filename)
#     try:
#         os.remove(path_image)
#     except:
#         ValueError(f"There's no {filename} in the directory")
