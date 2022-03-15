

from datetime import datetime

def search_v1(key_terms,location,Start_date,end_date,Timezone):
    #update start_date,end_date with timezone
    #data = select * from web data where start_date < startdate and enddate<end_date and locat = location
    # output = newdb
    # for i in key_terms:
    #   data = select info from data where info like %key_terms%
    #   insert into output select * from data
    #   data = newdb
    #   Search_Frequentlykey_update_v1(key_terms)
    return {output:output}# [report_json] ?
def Search_Frequently_key_v1():
    #data = select history from server order by frequence limit 0,5
    return {keys:data}
def Search_Frequentlykey_update_v1(keys):
    #data = select key,frequence from history where key = keys
    if exists(data):
        #update history set frequence = data[1]+1 where key = keys
    else:
        #insert into history values(keys,1)
    return {is_success: True}
def Search_History_v1():
    #data = select history from server limit 0,5
    return {records:data}
