filter_by_date_mode = {"Last month": "Last month", "3 last months": "3 last months", "All": "All"}
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

filter_by_status_mode = {"Active": "Active", "Unanswered": "Unanswered", "Discussed": "Discussed", "Closed": "Closed", "All": "All"}
filter_by_search_mode = {"none": "none", "search": ""}
Questions_status = {"closed": "closed", "new": "new", "discussed": "discussed", "all": "all"}

def filter_by_search(list_of_dicts_fo_filter, searched_text) -> list:
    if searched_text == "":
        return list_of_dicts_fo_filter

    not_found_value = -1
    filtered_list = []

    for row in list_of_dicts_fo_filter:
        found_search_text_in_title = str(row["Title"]).find(str(searched_text))
        found_search_text_in_message = str(row["Message"]).find(str(searched_text))

        if found_search_text_in_message != not_found_value or found_search_text_in_title != not_found_value:
            filtered_list.append(row)

    return  filtered_list

def filter_by_status(list_to_filter, filter_status) -> list:
    if filter_status == "all":
        return list_to_filter

    filtered_list = []
    if filter_status == "active":
        for row in list_to_filter:
            if row["Status"] == Questions_status["new"] or row["Status"] == Questions_status["discussed"] :
                filtered_list.append(row)
        return filtered_list

    for row in list_to_filter:
        if row["Status"] == filter_status:
            filtered_list.append(row)
    return filtered_list

def filter_by_date(list_of_dicts_to_filter, this_filter_by_date_mode) -> list:

    new_filtered_list = []
    if this_filter_by_date_mode == filter_by_date_mode["Last month"]:
        date_last_month_ago = datetime.now() + relativedelta(months=-1)
    elif this_filter_by_date_mode == filter_by_date_mode["3 last months"]:
        date_last_month_ago = datetime.now() + relativedelta(months=-3)
    elif this_filter_by_date_mode == filter_by_date_mode["All"]:
        return list_of_dicts_to_filter

    for row in list_of_dicts_to_filter:
        if row["Submission Time"] >= date_last_month_ago:
            new_filtered_list.append(row)

    return new_filtered_list

