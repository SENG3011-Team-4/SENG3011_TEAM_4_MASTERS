#import sys
#sys.path.append('../API_SourceCode')
import pymongo
from pymongo import MongoClient
from database import *
from Search import *

cluster = MongoClient("mongodb+srv://team4masters:uXTbGOYCXJTwTlIN@cluster0.d2xyd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["API-Database"]
rpts = db["Reports"]
hist = db["History"]
keyTerms = db["Key-Terms"]

def emptyCollections():
    rpts.delete_many({})
    hist.delete_many({})
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
    emptyCollections()
    addSampleRpts()
    testFind()
    #reports = rpts.find({"key_terms": {"$in": ["Zika"]}})
    #for report in reports:
    #    print(report)



