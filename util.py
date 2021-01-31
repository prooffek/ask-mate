import calendar, time, os
from pathlib import Path
from datetime import datetime
import data_manager


path = f"{Path(__name__).parent}/sample_data"
IMAGE_PATH = "/static/users_images"
IMAGE_FOLDER_PATH = f"{Path(__name__).parent}{IMAGE_PATH}"


def todays_date():
    return calendar.timegm(time.gmtime())


def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_image(image):
    image.save(os.path.join(IMAGE_FOLDER_PATH, image.filename))


def delete_image(image):
    path_image = os.path.join(IMAGE_FOLDER_PATH, image)
    try:
        os.remove(path_image)
    except:
        ValueError(f"There's no {image} in the directory")

def take_out_of_the_list(list):
    try:
        return list[0]
    except:
        pass

def question_tags_names(question_id) -> "RealDictCursor":
    tags = data_manager.get_nonquestion_by_question_id(question_id, data_manager.QUESTION_TAG_TABLE_NAME)
    return [take_out_of_the_list(data_manager.get_tag_by_id(tag["tag_id"]))
                     for tag in tags]

def get_tags_from_dict(dictionary):
    not_tags_keys = ["name", "title", "message", "id", "submission_time", "vote_number", "view_number", "image", "answers_number", "status"]
    return [value for key, value in dictionary.items() if key not in not_tags_keys]

def add_new_tags_to_db(tags_list):
    current_tags_list = [tag["name"] for tag in data_manager.get_tags_names()]
    [data_manager.add_tag(tag) for tag in tags_list if tag not in current_tags_list and tag != ""]

def add_question_tag_to_db(question_id, data_from_form):
    tags_selected = get_tags_from_dict(data_from_form)
    add_new_tags_to_db(tags_selected)
    tags_with_id = data_manager.get_tags_with_ids()

    [data_manager.add_question_tag(question_id, tag["id"]) for tag in tags_with_id if tag["name"] in tags_selected]

def update_question_tags(question_id, data_from_form):
    data_manager.del_question_tag(question_id)
    add_question_tag_to_db(question_id, data_from_form)

def users_id(session):
    try:
        return session["user_id"]
    except:
        return False