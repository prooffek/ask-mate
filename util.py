import calendar, time


def todays_date():
    return calendar.timegm(time.gmtime())
