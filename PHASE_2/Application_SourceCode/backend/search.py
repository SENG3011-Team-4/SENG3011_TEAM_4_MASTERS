from datetime import datetime, timedelta
from tempfile import tempdir
import snscrape.modules.twitter as sntwitter
from bs4 import BeautifulSoup
import requests
import time
import database as db
import re
import pandas as pd
import itertools

def search_v1(key_terms,location,start_date,end_date, timezone = "UTC", token = None):
    '''
    This function get requirements from users and return the Data that meets requirements
    Also those requirements will stored into search_his database
    '''

    # Split the key_terms string into list
    keyterms = key_terms.split(",")
    output = {}
    # Create a list to store the output
    output_dic = {}
    start_date_regex = re.match(r"(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2})",start_date)
    end_date_regex = re.match(r"(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2})",end_date)
    if start_date_regex is None or end_date_regex is None:
        raise ValueError("Date does not followed the format")
    
    #print(checkdate(start_date, end_date, "start"))
    if checkdate(start_date, end_date, "start"):
        raise ValueError("Start date is later than End date")
    
    if timezone != "UTC":
        start_date = check_timezone(start_date, timezone) # Standardize time
        end_date = check_timezone(end_date, timezone) # Standardize time
        # print("Standardised start date: ", start_date)
        # print("Standardised end date: ", end_date)
    
    for key in keyterms:
        #search_frequency_key_update_v1(key)
        db.update_frequent_keys(key)# update key terms search history
        # place input parameters into a dict and pass to the database
        params_dict = {
            "key_terms": key,
            "location": location,
            "start_date": start_date,
            "end_date": end_date
        }
        # database.py function to get reports
        search_result = db.get_reports(params_dict)
        try:
            for result in search_result:
                if result['headline'] not in output:
                    output[result['headline']] = 1
                    del result['_id']
                    output_dic[result['headline']] = result	
                else:
                    output[result['headline']] = output[result['headline']] + 1
        except:
            continue

    
    sorted_output = sorted(output.items(),key=lambda x: x[1],reverse=True)
    record_search = {
        "key_terms": key_terms,
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        "Timezone": timezone,
        "search_time": time.time()
    }

    if token != None:
        db.modify_history(record_search,token)

    returnlist = []
    for key in sorted_output:
        if output_dic[key[0]] != None:
            returnlist.append(output_dic[key[0]])
    
    return {
        "output": returnlist
    }

def search_frequency_key_v1():
    '''	
    Show the top five key terms searched by users
    '''
    results = db.get_frequent_keys()
    output = []
    for result in results:
        del result['_id']
        output.append(result)

    return {
        "top_five_keys": output
    }

def search_frequency_key_update_v1(keys):
    '''
    once have new search history, update the frequently key
    '''
    db.update_frequent_keys(keys)
    '''
    mydb = db.getdatabase()
    key_his = mydb.history.find_one({'key':keys})
    if key_his != None:
        mydb.history.update_one({'key':keys},{'$inc':{'frequence':1}})
    else:
        mydb.history.insert({'key':keys,'frequence':1})
    return {
        'is_success': True
    }
    '''

def search_history_v1(token):
    '''
    Records the last five searches
    '''
    results = db.get_history(token)
    output = []
    for result in results:
        del result['_id']
        output.append(result)
    return output

def check_timezone(date, Timezone):

    timezone_offset = Timezone[3:]
    hrs = int(timezone_offset[1:3])
    mins = int(timezone_offset[4:6])

    # TODO add regex for timezone string
    date = datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
    #print("Date before: ", date)
    if timezone_offset[0] == "+":
        # if UTC+01:00 is given, then we should minus 1 hr from the time to standardize to UTC
        date = date - timedelta(hours=hrs, minutes=mins)
        #print("Date after: ", date)
    elif timezone_offset[0] == "-":
        date = date + timedelta(hours=hrs, minutes=mins)
        #print(date)
    date = str(date).replace(" ", "T")
    return date

def checkdate(time1,time2,check):
    date_format = "%Y-%m-%dT%H:%M:%S"
    time_1 = datetime.strptime(time1, date_format)
    time_2 = datetime.strptime(time2, date_format)
    diff = time_1-time_2
    if diff.days > 0:
        if check == "start":
            return True
        else:
            return False
    else:
        if check == "start":
            return False
        else:
            return True

def search_twitter_v1(location, disease, no_items = 50):
    df_city = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
        '{} near:"{}" within:10km'.format(disease ,location)).get_items(), no_items))[['url', 'date','user','content', 'likeCount', 'quoteCount', 'retweetCount', 'replyCount']]
    
    return df_city.to_dict(orient='index')

def search_treatment_v1(disease):
    """
    Healthdirect live scraper.
    """

    # Search
    disease = disease.lower()
    if 'covid' in disease:
        pass
    search_url = f"https://www.healthdirect.gov.au/search-results/{disease}"
    data = requests.get(search_url)
    html = BeautifulSoup(data.text, 'html.parser')
    first_result = html.find("div", class_ = "veyron-local-search-results-list").find_all('a')[0]['href']

    # Extract
    final_link = f"https://www.healthdirect.gov.au{first_result}"
    data = requests.get(final_link)
    html = BeautifulSoup(data.text, 'html.parser')
    treated_start = html.find('h2', {"id": "treatment"}).next_element.next_element
    treated_end = treated_start.find_next("h2")
    html_list = []
    while treated_start != treated_end:
        temp_str = str(treated_start)
        if '<' in temp_str:
            if "ul" in temp_str and 'li' in temp_str:
                html_list.append(str(treated_start))
            if '<p>' in temp_str :
                html_list.append(str(treated_start))
        treated_start = treated_start.next_element
    html_string = "".join(html_list)
    
    return html_string

if __name__ == "__main__":
    search_treatment_v1("colds")

    
