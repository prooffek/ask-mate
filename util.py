import calendar, time
from datetime import datetime


def todays_date():
    return calendar.timegm(time.gmtime())


def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
