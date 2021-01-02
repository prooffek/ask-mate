filter_by_date_mode = {"last_month":1, "last_3_months":2,"all_time":4}
filter_by_status_mode = {"active": 1, "active: new": 2, "active: discussed": 3, "closed": 4}
filter_by_search_mode = {"none": 1, "search_text":""}



def filter_by_search(list_of_dicts_fo_filter, filter_by_date_mode) -> list:
    return list_of_dicts_fo_filter[1:5]

def filter_by_status(list_of_dicts_to_filter, filter_by_status_mode) -> list:
    return list_of_dicts_to_filter[1:5]

def filter_by_date(list_of_dicts_to_filter, filter_by_search_mode) -> list:
    return  list_of_dicts_to_filter[1:5]

