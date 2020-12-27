import csv
from pathlib import Path
from datetime import datetime

class csv_question_headers:
    id = "id"
    submission_time = "submission_time"
    view_number = "view_number"
    vote_number = "vote_number"
    title = "title"
    message = "message"
    image = "image"



path = f"{Path(__name__).parent}/sample_data"



def read_from_file(filename):
    filename = f"{path}/{filename}"

    data = []
    tmp_data = []
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            tmp_data.append(row)

    keys = tmp_data[0]
    for element in tmp_data[1:]:
        tmp_dict = {}
        for i in range(len(keys)):
            tmp_dict[keys[i]] = element[i]
        data.append(tmp_dict)

    return data

def convert_timestamp_to_date_format(table: list) -> list:
    for row in table:
        row[csv_question_headers.submission_time] = datetime.fromtimestamp(int(row[csv_question_headers.submission_time]))
    return table

def convert_date_to_timestamp_format(table: list) -> list:
    for row in table:
        row[csv_question_headers.submission_time] = int(datetime.timestamp((row[csv_question_headers.submission_time])))
    return table

def append_to_file(filename, dict_to_add):
    filename = f"{path}/{filename}"

    list_of_values = list(dict_to_add.values())
    content_to_add = ",".join(list_of_values) + "\n"

    try:
        f = open(filename, "a")
        f.write(content_to_add)
        f.close()
        print("The question/answer has been added successfully.")
    except:
        ValueError("An error has occured. Question/Answer has not been added.")

def write_to_file(filename, list_of_dicts_to_save, csv_separator = ','):
    try:
        filename = f"{path}/{filename}"
        list_of_dicts_to_save = connection.convert_date_to_timestamp_format(list_of_dicts_to_save)
        with open(filename, mode="w",  newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=csv_separator, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(list_of_dicts_to_save[0].keys())
            for record in list_of_dicts_to_save:
                row = record.values()
                csv_writer.writerow(row)
    except IOError:
        print(f"IOError while trying to open {filename} to write.")


