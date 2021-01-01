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


def append_to_file(filename, dict_to_add):
    filename = f"{path}/{filename}"

    list_of_values = list(dict_to_add.values())
    # content_to_add = ",".join(list_of_values) + "\n"

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
        with open(filename, mode="w",  newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=csv_separator, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(list_of_dicts_to_save_new[0].keys())
            for record in list_of_dicts_to_save_new:
                row = record.values()
                csv_writer.writerow(row)
    except IOError:
        print(f"IOError while trying to open {filename} to write.")

#answers = read_from_file("answer.csv")
#write_to_file("answer.csv", answers)


def image_to_file(image):
    image.save(os.path.join(IMAGE_FOLDER_PATH, image.filename))
