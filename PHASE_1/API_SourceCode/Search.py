
import pymongo
from datetime import datetime, timedelta
import time
from database import *
import re
def search_v1(key_terms,location,start_date,end_date,Timezone = "UTC",token):
	'''
	This function get requirements from users and return the Data that meets requirements
	Also those requirements will stored into search_his database
	'''
	#mydb = getdatabase()

	keyterms = key_terms.split(",") # Split the key_terms string into list
	output = {} # Create a list to store the output
	output_dic = {}
	if (re.match(r"(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2})",start_date) is None) or (re.match(r"(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2})",end_date) is None):
  		raise ValueError("Date does not followed the format")
	if checkdate(start_date,end_date,"start"):
  		raise ValueError("Start date is later than End date")
	if Timezone != "UTC":
		start_date = Check_Timezone(start_date,Timezone) # Standardize time
		#print("Standardised start date: ", start_date)
		end_date = Check_Timezone(end_date,Timezone) # Standardize time
		#print("Standardised end date: ", end_date)
	print("Keyterms: ", keyterms)
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

		#try:
			#for result in search_result:
				#print(result)
		#except:
			#print("Error encountered")
		try:
			for result in search_result:
				#print(result)
				if result['headline'] not in output:
					output[result['headline']] = 1
					del result['_id']
					output_dic[result['headline']] = result	
				else:
					output[result['headline']] = output[result['headline']] + 1
		except:
			print("Noting found")

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
	if token != None:
		modify_history(record_search,token)
	#if "search_his" in mydb.list_collection_names():
	#	mydb.search_his.insert(record_search)	# update search history
	#else:
    #	mydv["search_his"]
    #	mydb.search_his.insert(record_search)

	returnlist = []
	#for key in sorted_output:
	#	returnlist.append(key)
	#final_output = []
	for key in sorted_output:
		#print(key[0]
		if output_dic[key[0]] != None:
			#print(key[1])
			returnlist.append(output_dic[key[0]])
	#for key in output_dic.items():
	#	print(key)
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
	results = get_frequent_keys()
	output = []
	for result in results:
		del result['_id']
		output.append(result)
	return output

def Search_Frequentlykey_update_v1(keys):
	'''
	once have new search history, update the frequently key
	'''
    #data = select key,frequence from history where key = keys
	mydb = getdatabase()
    
	key_his = mydb.history.find_one({'key':keys})
    
	if key_his != None:
		mydb.history.update_one({'key':keys},{'$inc':{'frequence':1}})
	else:
		mydb.history.insert({'key':keys,'frequence':1})
    
	return {'is_success': True}
def Search_History_v1(token):
	'''
	Records the last five searches
	'''
    #data = select history from server limit 0,5
    #output = []
    #mydb = getdatabase()
    

    #for his in mydb.search_his.find().sort('search_time',pymongo.ASCENDING).limit(5)
    #	output.append(his) 
    
    #return {"records":output}#return a list of dic
	results = get_history(token)
	output = []
	for result in results:
		del result['_id']
		output.append(result)
	return output


#def getdatabase():
#	return pymongo.MongoClient('change this')

def Check_Timezone(date,Timezone):
	timezone_offset = Timezone[3:]
	hrs = int(timezone_offset[1:3])
	mins = int(timezone_offset[4:6])

	#TODO add regex for timezone string

	date = datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
	#print("Date before: ", date)
	if timezone_offset[0] == "+":
		# if UTC+01:00 is given, then we should minus 1 hr from the time to standardize to UTC
		date = date - timedelta(hours=hrs, minutes=mins)
		#print("Date after: ", date)
	elif timezone_offset[0] == "-":
		date = date + timedelta(hours=hrs, minutes=mins)
		#print(date)
	return date



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
if __name__ == '__main__':
    #print(search_v1("Zika,MERS,Anthrax","Sydney","2015-05-02T12:12:12","2020-05-02T12:12:12"))
    #print(search_v1("Zika","Sydney","2015-05-02T12:12:12","2020-05-02T12:12:12"))
    #print(search_v1("MERS","Sydney","2015-05-02T12:12:12","2020-05-02T12:12:12"))
    print("#######################################################################")
    print(search_v1("Study had","United States","2015-05-02T15:12:12","2025-05-02T15:12:12","UTC"))
    #print(Search_Frequently_key_v1())
    #print(Search_History_v1())
    # print(__name__)
    #Check_Timezone("2020-05-02T12:12:12", "UTC+01:15")
