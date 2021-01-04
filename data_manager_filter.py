# filter_by_date_mode = ["Last month", "3 last months","All time"]
# filter_by_status_mode = ["Active", "Active: New", "Active: Discussed", "Closed", "All"]
# filter_by_search_mode = ["none"]

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def filter_by_search(list_of_dicts_fo_filter, filter_by_search_mode) -> list:
    return  list_of_dicts_fo_filter



def filter_by_status(list_of_dicts_to_filter, filter_by_status_mode) -> list:
    return list_of_dicts_to_filter

def filter_by_date(list_of_dicts_to_filter, filter_by_date_mode) -> list:

    new_filtered_list = []
    if filter_by_date_mode == "Last month":
        date_last_month_ago = datetime.now() + relativedelta(months=-1)
    elif filter_by_date_mode == "3 last months":
        date_last_month_ago = datetime.now() + relativedelta(months=-3)
    elif filter_by_date_mode == "All time":
        return list_of_dicts_to_filter

    for row in list_of_dicts_to_filter:
        if row["Submission Time"] >= date_last_month_ago:
            new_filtered_list.append(row)

    return new_filtered_list

#new_filtered_list = filter_by_search()
