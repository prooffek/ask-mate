import csv
from pathlib import Path

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