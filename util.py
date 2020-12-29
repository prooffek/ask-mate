from datetime import datetime


def current_datetime():
    return datetime.now()


def convert_date_to_timestamp(date):
    return int(datetime.timestamp(date))
