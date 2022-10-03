#!/usr/bin/env python3

from tkinter import E
import pymongo
from bson.objectid import ObjectId
import os
import datetime
from datetime import date


PATH = "/home/pi/PhilAtHome/data/lightTime.txt"
DBSTRING = os.environ.get("DBSTRING")


def OpenFile():
    data = []

    if os.path.exists(PATH):

        with open(PATH, "r") as f:
            #print(f.read()
            print("TEST")
            data = [line.rstrip('\n').lstrip('\n') for line in f.readlines()]
            for entry in data: 
                print(entry)
           
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
    print(data)
    

    for entry in data: 
        print("TESTING SPLITTING", entry.split(" "))
        dayTime = (entry.replace("\\n", "").split(" "))
        if dayTime != None or dayTime != [""]: #or dayTime[1] != "" or dayTime != "":
            print("CURENTDAYTIME", dayTime)
            try: 
                day, time = dayTime[0], dayTime[1]
            except:
                break
            mydict = {"Day": day, "LightTimeToday": datetime.datetime.strptime(time, "%H:%M:%S")}

            mydb.insert_one(mydict)
    os.remove(PATH)


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
                "Day": {"$gte": str(dateWeekAgo), "$lte": str(dateToday)}}}])
            #{"$group": {"_id": "null", "LightTimeToday": {"$dateToString":{format: "%H-%M-&S"} }}}])

    )
    #print(doc)
    resultTime = []
    for time in doc: 
        timeIndividual = (time['LightTimeToday'])
        test = datetime.datetime.strftime(timeIndividual, "%H:%M:%S").split(" ")
        resultTime.append(datetime.datetime.strptime(test[0], "%H:%M:%S").time())
    totalTime = datetime.timedelta(hours=0,minutes=0,seconds=0)
    for finalTime in resultTime: 
        h,m,s = SpliceTime(finalTime)
        totalTime += datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    print(resultTime)
    print("FinalTime: ", totalTime)
    time = doc[0]["LightTimeToday"]  # Get the time from the document
    print("time", time)
    # Return the data
    return totalTime

def SpliceTime(time): 
    timeStr = str(time)
    h,m,s = timeStr.split(":")
    return h,m,s
if __name__ == "__main__": 
    try:
        ConnToDb()
        print("Connected to the DB")
    except Exception as e:
        print(e)
        print("Could not connect to the DB")
        exit(3)

