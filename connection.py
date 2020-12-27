import csv


def read_from_file(filename):

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