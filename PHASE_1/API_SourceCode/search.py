from datetime import datetime, timedelta
import time
import database as db
import re

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
    return output

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

def check_timezone(date,Timezone):
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

if __name__ == '__main__':
	print (checkdate("2025-10-01T08:45:10","2016-10-01T08:45:10","start"))
