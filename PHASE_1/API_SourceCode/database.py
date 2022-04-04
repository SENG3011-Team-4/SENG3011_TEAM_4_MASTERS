import pymongo
from pymongo import MongoClient
#from scraper import web_data
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
	if(Session.find_one({"u_id":session_data["u_id"]}) is None):
		Session.insert_one(session_data)
	return

def check_session_by_token(token):
	return Session.find_one({"token":token})

def user_list():
	return User.find()
def delete_session(token):

	Session.delete_one({"token":token})
	return
# ===================================================

def clearAll():
    rpts.delete_many({})
    hist.delete_many({})
    keyTerms.delete_many({})
    User.delete_many({})
    Session.delete_many({})

def toggleTests(testMode):
    # switch database to testing database to not interfere with any existing data upon deployment
    if testMode:
        db = cluster["Test-Database"]
    else:
        db = cluster["API-Database"]
    global rpts
    rpts = db["Reports"]
    global hist
    hist = db["History"]
    global keyTerms
    keyTerms = db["KeyTerms"]
    global User
    User = db["User"]
    global Session
    Session = db["Session"]

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

"""
def get_reports(args):
    # Current algorithm:
    # Search to find whether any of the key terms exist within the headline, main text of article or diseases in reports
    # Then check whether the reports have locations and dates matching the specified date and location of the search
	
    results = rpts.find(
                {"$and":[
                        # Matching any article with a disease in the disease list
                        {"report":{"$elemMatch":{"diseases":{"$elemMatch":{ "$regex": args["key_terms"], "$options": "i"}}}}},
                
                        # AND an event date within the start-end date range
			            #{"date_of_publication":{"$gt": args["start_date"], "$lt": args["end_date"]}},      

                        # TODO: confirm whether we will have an event date or will use date of publication as date range
                        #{"report":{"$elemMatch":{"event_date":{"$elemMatch":{"$gt": args["start_date"], "$lt": args["end_date"]}}}}},

                        # AND location matching a country OR city as specified
                        {"$or": [{"report":{"$elemMatch":{"locations":{"$elemMatch":{"country":{"$elemMatch":{"$regex": args["location"]}}}}}}},
                                {"report":{"$elemMatch":{"locations":{"$elemMatch":{"cities":{"$elemMatch":{"$regex": args["location"]}}}}}}}
                                ]}
                ]}

		#{"reports":{"event_date":{"$gt": "2015-05-02T12:12:12", "$lt": "2020-05-02T12:12:12"}}}
		)
    
    results = rpts.find(
                        {"$and":[
                                {"report":{"$elemMatch":{"disease":{"$elemMatch":{ "$regex": "covid-19", "$options": "i"}}}}},
                                {"$or": [{"report":{"$elemMatch":{"locations":{"$elemMatch":{"country":{"$elemMatch":{"$regex": "United States"}}}}}}},
                                        {"report":{"$elemMatch":{"locations":{"$elemMatch":{"cities":{"$elemMatch":{"$regex": "United States"}}}}}}}
                                        ]}
                                ]
                        }
    )

    print(args)
    return results
"""

def get_reports(args):
    results = rpts.find(
                        {"$and":[
                                {"report":{"$elemMatch":{"disease":{"$elemMatch":{ "$regex": args["key_terms"], "$options": "i"}}}}},
                                {"date_of_publication":{"$gt": args["start_date"], "$lt": args["end_date"]}},      
                                {"$or": [{"report":{"$elemMatch":{"locations":{"$elemMatch":{"country":{"$elemMatch":{"$regex": args["location"], "$options": "i"}}}}}}},
                                        {"report":{"$elemMatch":{"locations":{"$elemMatch":{"cities":{"$elemMatch":{"$regex": args["location"], "$options": "i"}}}}}}}
                                        ]}
                                ]
                        }
    )
    return results



def get_frequent_keys():
    # returns 5 most frequent keys, alphabetically if there are results with equal frequency
    return keyTerms.find().sort("key", pymongo.ASCENDING).sort( "frequency", pymongo.DESCENDING ).limit(5)

def update_frequent_keys(key):
    # TODO: enforce data integrity
    # === DATA STRUCTURE ===
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

def get_history(token):
    return hist.find({"token":token}).sort( "time", pymongo.DESCENDING ).limit(5)

def modify_history(search_record,token):
	# TODO
	# should change db format from list of dic to      dic of list of dic,
	# TODO: enforce data integrity
	
	
    # not sure if searching a database starts is FIFO or LIFO, need to double check in testing
    hist.insert_one({
		    "his": search_record, 
		    "token":token,
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

