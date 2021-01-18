import calendar, time, os
from pathlib import Path
from datetime import datetime


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