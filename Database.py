import pymongo
from bson.objectid import ObjectId
import os
import datetime
from datetime import date


PATH = "/data.txt"
DBSTRING = os.environ.get("DBSTRING")

def OpenFile():
    with open(PATH, "r") as f:
        data = f.readline()
        data.split(" ")
        return data


def ConnToDb():
    myClient = pymongo.MongoClient(
        DBSTRING
    )
    mydb = myClient["PhilAtHome"]
    coll = mydb["time"]


    return coll

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
    # Connect to the database
    coll = ConnToDb()

    # Get the date from today and from a week ago
    dateToday = date.today()
    dateWeekAgo = dateToday - datetime.timedelta(days=7)

    # Fetch the data from the database that is between the two dates
    doc = list(
        coll.aggregate([
            {"$match": {"Day": {"$gte": dateWeekAgo, "$lte": dateToday}}},
            {"$group": {"_id": "null", "LightTimeToday": {"$sum": "$LightTimeToday"}}}])

    )

    time = doc[0]["LightTimeToday"]  # Get the time from the document

    # Return the data
    return time
