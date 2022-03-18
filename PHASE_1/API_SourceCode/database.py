import pymongo
from pymongo import MongoClient

# Accessing database from the cloud
cluster = MongoClient("mongodb+srv://team4masters:uXTbGOYCXJTwTlIN@cluster0.d2xyd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["API-Database"]
rpts = db["Reports"]
hist = db["History"]
keyTerms = db["KeyTerms"]

"""
# ==== WRITING DATA ====

# Data is uploaded to the database using "posts"

post = {"_id": 0, "url": art_url, "date_of_publication": date, "headline": headline, "main_text": main_text, "report": reports}

# use insert_many to insert multiple posts to the database
# rpts.insert_many([post1, post2])

# similar for deleting

# deletes all entries that match
rpts.delete_many({"field": "blyat"})

# ==== SEARCHING DATA ====

results = rpts.find({"field": desired_field})

for result in results:
    print(result)          # prints the entire dict of the result
    print(result({"_id"})) # prints specific field from the result

# find a singular result, returns the dict rather than the Mongo object
results = rpts.find_one({"field": desired_field})

# returns all entries in the db
results = rpts.find({})

# ==== UPDATING DATA ====

# first parameter is the records which should be updated, the second is what operation should be performed
# examples are https://docs.mongodb.com/manual/reference/operator/update/
results = rpts.update_many({"field": blyat}, {"$set":{"name": "tim"}})
"""

def write_report(reports):
    """
    Writes a disease report to the reports collection

    :param reports: list of dictionaries
    report = {
        key_terms,
        location,
        date,
    }
    :param param2: this is a second param
    :returns: this is a description of what is returned
    :raises keyError: raises an exception
    """
    rpts.insert_many(reports)

def get_reports(args):
    return rpts.find({
        "key_terms": { "$in": args["key_terms"] },
        "location": args["location"],
        "date": { "$gt": args["start_date"], "$lt": args["end_date"]}
    })

def get_frequent_keys():
    #return keyTerms.find({}).sort({"frequency": -1}).limit(5)
    return keyTerms.find().sort("key", pymongo.ASCENDING).sort( "frequency", pymongo.DESCENDING ).limit(5)

def update_frequent_keys(key):
    keys = keyTerms.find_one({"key": key})
    if keys != None:
        keyTerms.update_one({"key": key}, {"$inc": {"frequency":1}})
    else:
        keyTerms.insert_one({
            "key": key, 
            "frequency": 1
        })

def get_history():
    return hist.find({}).sort("search_time", pymongo.ASCENDING).limit(5)

def modify_history(search_record):
    # not sure if searching a database starts is FIFO or LIFO, need to double check in testing
    hist.insert_one(search_record)

    
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