
from tkinter import E
import pymongo
from bson.objectid import ObjectId
import os
import datetime
from datetime import date


PATH = "data/lightTime.txt"
DBSTRING = os.environ.get("DBSTRING")


def OpenFile():
    if os.path.exists(PATH):
        with open(PATH, "r") as f:
            data = f.readline()
            data.split(" ")
            return data
    else:
        return None


def ConnToDb():
    myClient = pymongo.MongoClient(
        DBSTRING
    )
    mydb = myClient["PhilAtHome"]
    coll = mydb["time"]

    return coll


def insertToDb():
    mydb = ConnToDb()
    data = OpenFile()

    data = data.split(" ")  # split the data by the space
    mydict = {"Day": data[0], "LightTimeToday": int(data[1])}

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
            {"$match": {
                "Day": {"$gte": str(dateWeekAgo), "$lte": str(dateToday)}}},
            {"$group": {"_id": "null", "LightTimeToday": {"$sum": "$LightTimeToday"}}}])

    )

    time = doc[0]["LightTimeToday"]  # Get the time from the document

    # Return the data
    return time


if __name__ == "__main__":
    try:
        OpenFile()

    except Exception as e:
        print(e)
