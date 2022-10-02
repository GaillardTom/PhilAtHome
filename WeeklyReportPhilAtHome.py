from SendSMS import SendSMS, SendWeeklyLog
from Database import FetchData

CLIENT_PHONE = "+33 7 67 02 75 15"


def CheckWeeklyLightTime():
    data = FetchData()  # get the data from the file
    data = data.split("\r")  # split the data by the new line
    lightTime = 0
    for line in data:
        if line != "":
            line = line.split(",")  # split the line by the comma
            lightTime = lightTime + int(line[1])  # add the light time to the total light time
    print("Total light time for the week: " + str(lightTime))  # print the total light time   
    SendWeeklyLog(CLIENT_PHONE, lightTime)  # send the weekly log to the email