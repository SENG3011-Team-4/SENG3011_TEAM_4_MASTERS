# Backend functions for Phase 2

import search as search
import database as db
from datetime import datetime, timedelta
import time
import json



def common_disease_search(location):
    """
    Finds the most common diseases at that location, which can then be used to match vaccines and medications recommended for travelling
    """

    # === load in most frequent diseases to search ===
    disease_list_json = open('disease_list.json')
    disease_list = json.load(disease_list_json)


    # === construct dates in which to look for articles ===
    end_date = time.time()
    dt_end_date = datetime.fromtimestamp(end_date)
    dt_start_date = dt_end_date - timedelta(days=(10*365.25))  # start date is 10 years before end date

    # convert datetimes to strings
    str_end_date = str(dt_end_date).replace(" ", "T")
    str_end_date = str_end_date[:19]
    str_start_date = str(dt_start_date).replace(" ", "T")
    str_start_date = str_start_date[:19]

    frequency_list = []
    # === begin searching most common diseases and keep track of the 5 which have the most articles ===
    for disease in disease_list:
        article_results = search.search_v1(disease, location, str_start_date, str_end_date)
        if len(frequency_list) < 5:
                frequency_list.append({
                    "disease": disease,
                    "frequency": len(article_results)
                })
        else:
            # compare to the current list of 5 most frequent
            if len(article_results) > frequency_list[0]["frequency"]:
                # remove least frequent element and replace
                frequency_list.pop(0)
                frequency_list.append({
                    "disease": disease,
                    "frequency": len(article_results)
                })
                # sort the list into ascending order so least frequent is at the start
                frequency_list = sorted(frequency_list, key=lambda k: k["frequency"])

    return frequency_list

def vaccine_match():
    """
    Matches vaccines and medications to diseases frequently reported at the location
    """
    
    # TODO: implement scraper to find vaccine


if __name__ == "__main__":
    common_disease_search("ha")