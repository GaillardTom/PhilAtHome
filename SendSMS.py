
#!/usr/bin/env python3

import os
from twilio.rest import Client


# Send a SMS with the twillio API using python3


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
client = Client(account_sid, auth_token)
CLIENT_PHONE = os.environ.get("CLIENT_PHONE")

def SendSMS(numToSend, temp, timeDate, error=False): 
    if error:
        messageBody = "Error: Please restart the service or contact an admin DATETIME: " + timeDate
    else:
        messageBody = "The temperature is " + \
            str(temp) + " degrees at " + timeDate
    message = client.messages \
                    .create(
                        body=messageBody,
                        from_='+19895751665',
                        to=numToSend
                    )

    print(message.sid)

def SendWeeklyLog(numToSend, timePassed):
    messageBody = "You have spent " + str(timePassed) + " with the lights on this week"
    message = client.messages \
                    .create(
                        body=messageBody,
                        from_='+19895751665',
                        to=numToSend
                    )

    print(message.sid)
    
    


    print(message.sid)


if __name__ == "__main__":
    try:
        SendSMS(CLIENT_PHONE, 25, "12:00 Sept 9 2022")
    except:
        print("Error")
