#import sys
#sys.path.append('../API_SourceCode')
import pymongo
from pymongo import MongoClient
import time
from database import *
from Search import *

cluster = MongoClient("mongodb+srv://team4masters:uXTbGOYCXJTwTlIN@cluster0.d2xyd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["API-Database"]
rpts = db["Reports"]
hist = db["History"]
keyTerms = db["KeyTerms"]
"""
def emptyCollections():
    #rpts.delete_many({})
    #hist.delete_many({})
    keyTerms.delete_many({})

def addSampleRpts():
    sample_art_1 = {
        "key_terms": ["Anthrax", "Zika"],
        "location": "Sydney",
        "date": "2018-05-02T12:12:12"
    }
    sample_art_2 = {
        "key_terms": ["Outbreak", "MERS"],
        "location": "Sydney",
        "date": "2018-10-02T12:12:12"
    }
    write_report([sample_art_1, sample_art_2])

def testFind():
    args = {
        "key_terms": ["Anthrax", "Zika"],
        "location": "Sydney",
        "start_date": "2015-05-02T12:12:12",
        "end_date": "2020-05-02T12:12:12",
    }
    search_v1("Zika", args["location"], args["start_date"], args["end_date"])
    #reports = get_reports(args)
    #for report in reports:
    #    print(report)    

if __name__ == "__main__":
    #emptyCollections()
    #addSampleRpts()
    testFind()
    results = get_frequent_keys()
    for result in results:
        print(result)
    #reports = rpts.find({"key_terms": {"$in": ["Zika"]}})
    #for report in reports:
    #    print(report)
"""

def test_write_report():

    # reset state to ensure this entry does not exist
    rpts.delete_many({
        "key_terms": ["Anthrax", "Zika"],
        "location": "Sydney",
        "date": "2018-05-02T12:12:12"
    })

    args = [{
        "key_terms": ["Anthrax", "Zika"],
        "location": "Sydney",
        "date": "2018-05-02T12:12:12"
    }]
    write_report(args)
    assert rpts.find_one({
        "key_terms": ["Anthrax", "Zika"],
        "location": "Sydney",
        "date": "2018-05-02T12:12:12"
    })

def test_get_reports():

    # reset state to ensure this entry does not exist
    rpts.delete_many({
        "key_terms": ["Anthrax", "Zika"],
        "location": "Sydney",
        "date": "2018-05-02T12:12:12"
    })

    args = [{
        "key_terms": ["Anthrax", "Zika"],
        "location": "Sydney",
        "date": "2018-05-02T12:12:12"
    }]

    write_report(args)
    assert rpts.find_one({
        "key_terms": ["Anthrax", "Zika"],
        "location": "Sydney",
        "date": "2018-05-02T12:12:12"
    })
    args = {
        "key_terms": ["Anthrax", "Zika"],
        "location": "Sydney",
        "start_date": "2015-05-02T12:12:12",
        "end_date": "2020-05-02T12:12:12",
    }
    result = get_reports(args)
    assert result[0] != None


def test_update_frequent_keys():
    keyTerms.delete_many({"key": "Test Case 1"})
    keyTerms.delete_many({"key": "Test Case 2"})

    update_frequent_keys("Test Case 1")
    assert keyTerms.find_one({"key": "Test Case 1"}) != None

    results = get_frequent_keys()
    for result in results:
        print(result)

    update_frequent_keys("Test Case 1")
    assert keyTerms.find_one({"key": "Test Case 1", "frequency": 2}) != None

    results = get_frequent_keys()
    for result in results:
        print(result)

    update_frequent_keys("Test Case 2")
    assert keyTerms.find_one({"key": "Test Case 2"}) != None

    results = get_frequent_keys()
    for result in results:
        print(result)

    keyTerms.delete_many({"key": "Test Case 1"})
    keyTerms.delete_many({"key": "Test Case 2"})

def test_sorted_keys():
    
    # test that the frequent keys are correctly sorted in order of frequency

    keyTerms.delete_many({"key": "Test Case 1"})
    keyTerms.delete_many({"key": "Test Case 2"})

    update_frequent_keys("Test Case 1")
    assert keyTerms.find_one({"key": "Test Case 1"}) != None

    update_frequent_keys("Test Case 1")
    assert keyTerms.find_one({"key": "Test Case 1", "frequency": 2}) != None

    update_frequent_keys("Test Case 2")
    assert keyTerms.find_one({"key": "Test Case 2"}) != None

    results = get_frequent_keys()
    prev_freq = results[0]["frequency"]
    for result in results:
        # check that each entry has a higher frequency than the next
        if prev_freq < result["frequency"]:
            raise Exception("Frequent keys are not sorted correctly")
        prev_freq = result["frequency"]

def test_modify_history():
    hist.delete_many({
        "key_terms": ["Test Term 1", "Test Term 2"],
        "location": "Test Location",
        "start_date": "2015-05-02T12:12:12",
        "end_date": "2020-05-02T12:12:12",
		"Timezone": "UTC",
    })

    record_search = {
        "key_terms": ["Test Term 1", "Test Term 2"],
        "location": "Test Location",
        "start_date": "2015-05-02T12:12:12",
        "end_date": "2020-05-02T12:12:12",
		"Timezone": "UTC",
		"search_time": time.time()
	}

    modify_history(record_search)

    assert hist.find_one({
        "key_terms": ["Test Term 1", "Test Term 2"],
        "location": "Test Location",
        "start_date": "2015-05-02T12:12:12",
        "end_date": "2020-05-02T12:12:12",
		"Timezone": "UTC",
    }) != None

    hist.delete_many({
        "key_terms": ["Test Term 1", "Test Term 2"],
        "location": "Test Location",
        "start_date": "2015-05-02T12:12:12",
        "end_date": "2020-05-02T12:12:12",
		"Timezone": "UTC",
    })

if __name__ == "__main__":
    test_modify_history()

