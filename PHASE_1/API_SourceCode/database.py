import pymongo
from pymongo import MongoClient
from scraper import web_data
import time

# TODO:
# - specify data schema for each database
# - create some form of data security in each data base (any writes to databases should enforce the format)
# - setup and reset functionality for the database
# - clean up code, remove unnecessary commented out lines and section each part out
# - pydoc everything
# - integrate enforced data integrity into the web scraper

# =============== DATABASE SETUP ===================
cluster = MongoClient("mongodb+srv://team4masters:uXTbGOYCXJTwTlIN@cluster0.d2xyd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["API-Database"]

# reports collection handles all the article jsons, taking input from scraper and sending output to API calls
rpts = db["Reports"]
#rpts.insert_many(web_data)

# history collection records all interactions with the database to provide the user with data on what has been most recently searched for
hist = db["History"]

# keyterms collection records the most frequently searched terms
# TODO remove this collection and integrate functionality into history, doing a count of key terms in history
keyTerms = db["KeyTerms"]

# User collection stores all registered user information, hashed for security
User = db["User"]
# Session collection stores data on all currently logged in users to keep track of who is using the site
Session = db["Session"]
# ===================================================

# =============== AUTH FUNCTIONS ===================
def find_user_by_email(email):
	return User.find_one({"email":email})

def registed_user(user_data):
	User.insert_one(user_data)
	return

def Session_update(session_data):
	Session.insert_one(session_data)
	return

def check_session_by_token(token):
	return Session.find_one({"token":token})

def delete_session(token):
	#TODO
    pass
# ===================================================


def write_report(reports):
    # TODO: enforce the structure of the report to match the spec, example json is below
    for report in reports:
        rpts.insert_one(report)

# ==== EXAMPLE JSON ====
# {
#    "url": "https://www.who.int/csr/don/17-january-2020-novel-coronavirus-japan-ex-china/en/",
#    "date_of_publication": "2020-01-17 xx:xx:xx",
#    "headline": "Novel Coronavirus – Japan (ex-China)",
#    "main_text": "On 15 January 2020, the Ministry of Health, Labour and Welfare, Japan (MHLW) reported an imported case of laboratory-confirmed 2019-novel coronavirus (2019-nCoV) from Wuhan, Hubei Province, China. The case-patient is male, between the age of 30-39 years, living in Japan. The case-patient travelled to Wuhan, China in late December and developed fever on 3 January 2020 while staying in Wuhan. He did not visit the Huanan Seafood Wholesale Market or any other live animal markets in Wuhan. He has indicated that he was in close contact with a person with pneumonia. On 6 January, he traveled back to Japan and tested negative for influenza when he visited a local clinic on the same day.",
#    "reports": [
#       {
#          "event_date": "2020-01-03 xx:xx:xx to 2020-01-15",
#          "locations": [
#             {
#                "country": "China",
#                "location": "Wuhan, Hubei Province"
#             },
#             {
#                "country": "Japan",
#                "location": ""
#             }
#          ],
#          "diseases": [
#             "2019-nCoV"
#          ],
#          "syndromes": [
#             "Fever of unknown Origin"
#          ]
#       }
#    ]
# }


def get_reports(args):
    # Current algorithm:
    # Search to find whether any of the key terms exist within the headline, main text of article or diseases in reports
    # Then check whether the reports have locations and dates matching the specified date and location of the search
	results = rpts.find({
		"$or": [{"headline": {"$regex": args["key_term"], "$options": 'i'} }, 
				{"main_text": {"$regex": args["key_term"], "$options": 'i'} },
                {"reports":{"$elemMatch":{"diseases":{"$elemMatch'":{ "$regex": args["key_term"] }}}}},
			]},
			{"reports":{"$elemMatch":{"locations":{"$elemMatch'":{ "$regex": args["location"] }}}}},
		 {"reports":{"$elemMatch":{"event_date":{"$elemMatch":{"$gt": args["start_date"], "$lt": args["end_date"]}}}}}      
		#{"reports":{"event_date":{"$gt": "2015-05-02T12:12:12", "$lt": "2020-05-02T12:12:12"}}}
		)
	return results

def get_frequent_keys():
    # returns 5 most frequent keys, alphabetically if there are results with equal frequency
    return keyTerms.find().sort("key", pymongo.ASCENDING).sort( "frequency", pymongo.DESCENDING ).limit(5)

def update_frequent_keys(key):
    # TODO: enforce data integrity
    # keys in this database should have the structure:
    # key_example: {
    #   "key": string,
    #   "frequency": int
    # }
	keys = keyTerms.find_one({"key": key})
	if keys != None:
		keyTerms.update_one({"key": key}, {"$inc": {"frequency":1}})
	else:
		keyTerms.insert_one({
		    "key": key, 
		    "frequency": 1
		})
	return

def get_history():
    return hist.find({}).sort("search_time", pymongo.ASCENDING).sort( "time", pymongo.DESCENDING ).limit(5)

def modify_history(search_record,token):
	# TODO
	# should change db format from list of dic to      dic of list of dic,
	# TODO: enforce data integrity
	
	
    # not sure if searching a database starts is FIFO or LIFO, need to double check in testing
    hist.insert_one({
		    "his": search_record, 
		    "time": time.time()
		})
    
    #if history.len() > 5:
    #    # find the item with the earliest search time
    #    earliest = history[0]["search_time"]
    #    for item in history:
    #        if item["search_time"] < earliest:
    #            earliest = item["search_time"]
    #    hist.delete_one({"search_time": earliest})
    #    hist.insert_one(search_record)
    #else:
    #    hist.insert_one(search_record)
