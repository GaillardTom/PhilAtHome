import pymongo
from bson.objectid import ObjectId
import os 



PATH = "/data.txt"

def OpenFile():
    with open(PATH, "r") as f:
        data = f.readline()
        data.split(" ")
        return data


def ConnToDb():
    myClient = pymongo.MongoClient(
        "mongodb://localhost:27017"
    )
    mydb = myClient["PhilAtHome"]


    return mydb

def insertToDb():
    mydb = ConnToDb()
    data = OpenFile()
    
    mydict = {"Day": data[0], "LightTimeToday": data[1]}
    
    x = mydb.insert_one(mydict)
    os.remove(PATH)
    return ObjectId(x.inserted_id)

    
def FetchData():
    coll = ConnToDb()
    # df = pd.DataFrame(coll)
    doc = list(coll.find())