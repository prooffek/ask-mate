filter_by_date_mode = {"none":1,"hot_last_week":2, "hot_last_month":3,\
                       "hot_last_3months":4, "unanswered_this_week":5,\
                       "unanswered_this_month":6, "unanswered_more_then_month":7}
filter_by_status_mode = {"none": 1, "new": 2, "discussed": 3, "closed": 4, "active":5}
filter_by_search_mode = {"none": 1, "search_text":""}



def filter_by_search(list_of_dicts_fo_filter, filter_by_date_mode) -> list:
    return list_of_dicts_fo_filter[1:5]

def filter_by_status(list_of_dicts_to_filter, filter_by_status_mode) -> list:
    return list_of_dicts_to_filter[1:5]

def filter_by_date(list_of_dicts_to_filter, filter_by_search_mode) -> list:
    return  list_of_dicts_to_filter[1:5]

