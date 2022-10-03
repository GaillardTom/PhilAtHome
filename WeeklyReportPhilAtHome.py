#!/usr/bin/python3


from SendSMS import SendSMS, SendWeeklyLog
from Database import FetchData
import os
#CLIENT_PHONE = "+33 7 67 02 75 15"
CLIENT_PHONE = os.environ.get("CLIENT_PHONE")

def CheckWeeklyLightTime():
    data = FetchData()  # get the data from the file
    print("data", data)
    
    print("Total light time for the week: " + str(data))  # print the total light time   
    SendWeeklyLog(CLIENT_PHONE, (data))  # send the weekly log to the email

if __name__ == "__main__": 
    try: 
        CheckWeeklyLightTime()
    except Exception as e: 
        print(e)
        print("Error while sending SMS or checking log file")
        exit(4)
