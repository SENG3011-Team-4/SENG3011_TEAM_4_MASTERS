
import pymongo
from datetime import datetime
import time
from database import *
def search_v1(key_terms,location,start_date,end_date,Timezone = "UTC"):
	'''
	This function get requirements from users and return the Data that meets requirements
	Also those requirements will stored into search_his database
	'''
	mydb = getdatabase()

	keyterms = key_terms.split(",") # Split the key_terms string into list
	output = [] # Create a list to store the output

	if Timezone != "UTC":
		start_date = Check_Timezone(start_date,Timezone)#Standardize time
		end_date = Check_Timezone(end_date,Timezone)#Standardize time
	for key in keyterms:
		#Search_Frequentlykey_update_v1(key)
		update_frequent_keys(key)# update key terms search history

		# place input parameters into a dict and pass to the database
		params_dict = {
			"key_terms": key,
			"location": location,
			"start_date": start_date,
			"end_date": end_date
		}

		# database.py function to get reports
		search_result = get_reports(params_dict)
		
		#search_result = mydb.webdata.find({'$web_data': {'$search': key}},
		#						  {'$where': checkdate(obj.start_date,start_date,"start") == True},
		#						  {'$where': checkdate(obj.end_date,end_date,"end") == True},
		#						  {'location':location}) # Find all the web_data that match the requirements

		for result in search_result:
			if result['web_data'] not in output:
				output[result['web_data']] = 1	
			else:
				output[result['web_data']] = output[result['web_data']] + 1

	# 	alternate simple method to pass key_terms to database, but would need other way to count the number of matching key terms
	# 
	#	params_dict = {
	#		"key_terms": key_terms, # pass all key terms, and search once
	#		"location": location,
	#		"start_date": start_date,
	#		"end_date": end_date
	#	}
	#
	#	get_reports(params_dict)
	#	
	#	for 
	#

	
	sorted_output = sorted(output.items(),key=lambda x: x[1],reverse=True)
	record_search = {
		"key_terms":key_terms,
		"location":location,
		"start_date":start_date,
		"end_date":end_date,
		"Timezone":Timezone,
		"search_time":time.time()
	}

	modify_history(record_search)
	#if "search_his" in mydb.list_collection_names():
	#	mydb.search_his.insert(record_search)	# update search history
	#else:
    #	mydv["search_his"]
    #	mydb.search_his.insert(record_search)

	returnlist = []
	for key in sorted_output:
		returnlist.append(key)

	return {"output":returnlist} # [report_json] ?

def Search_Frequently_key_v1():
	'''	
	Show the top five key terms searched by users
	'''
    #data = select history from server order by frequence limit 0,5
	#output = []
	#mydb = getdatabase()
    
	#for his in mydb.history.find().sort('frequence',pymongo.ASCENDING).limit(5):
	#	output.append(his['key']) 
    	
	#return {"keys":output}
	return get_frequent_keys()

def Search_Frequentlykey_update_v1(keys):
	'''
	once have new search history, update the frequently key
	'''
    #data = select key,frequence from history where key = keys
	mydb = getdatabase()
    
	key_his = mydb.history.find_one({'key':keys})
    
	if key_his != None:
    	mydb.history.update_one({'key':keys},{$inc:{'frequence':1}})
	else:
    	mydb.history.insert({'key':keys,'frequence':1})
    
    return {'is_success': True}
def Search_History_v1():
	'''
	Records the last five searches
	'''
    #data = select history from server limit 0,5
    #output = []
    #mydb = getdatabase()
    

    #for his in mydb.search_his.find().sort('search_time',pymongo.ASCENDING).limit(5)
    #	output.append(his) 
    
    #return {"records":output}#return a list of dic

	return get_history()

#def getdatabase():
#	return pymongo.MongoClient('change this')

def Check_Timezone(date,Timezone):
	pass

def checkdate(time1,time2,check):

	date_format = "%Y-%m-%dT%H:%M:%S"
	time_1 = datetime.strptime(time1, date_format)
	time_2 = datetime.strptime(time2, date_format)
	diff = time_1-time_2
	if diff.seconds > 0:
		if check == "start":
			return True
		else:
			return False
	else:
		if check == "start":
			return False
		else:
			return True


