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

# jour quon est -7 jours, prend tous les collections a partir de jour -7 a aujourd'hui et ajouter tous les temps 
# pour display cette sem vs avez passez 


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
    doc = list(
        coll.aggregate([
        {"$match": {"_id": {"$week": "$Day"}}},
        {"$group": {"_id": "$Day", "LightTimeToday": {"$sum": "$LightTimeToday"}}}
        ]
    ))
    
    return doc

