from datetime import datetime
import calendar, time


def current_datetime():
    return datetime.now()


def convert_date_to_timestamp(date):
    return int(datetime.timestamp(date))


def todays_date():
    return calendar.timegm(time.gmtime())