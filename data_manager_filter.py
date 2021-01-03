filter_by_date_mode = {"Last month":1, "3 last months":2,"All time":4}
filter_by_status_mode = {"Active": 1, "Active: New": 2, "Active: Discussed": 3, "Closed": 4, "All":5}
filter_by_search_mode = {"none": 1, "search_text":""}



def filter_by_search(list_of_dicts_fo_filter, filter_by_date_mode) -> list:
    return list_of_dicts_fo_filter[1:5]

def filter_by_status(list_of_dicts_to_filter, filter_by_status_mode) -> list:
    return list_of_dicts_to_filter[1:5]

def filter_by_date(list_of_dicts_to_filter, filter_by_search_mode) -> list:
    return  list_of_dicts_to_filter[1:5]

