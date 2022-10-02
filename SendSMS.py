
import os
from twilio.rest import Client



#Send a SMS with the twillio API using python3


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = "AC7f6303642211a699497a29b1c6420bda"
auth_token = "f6a636c9c495f5cf943e08f0d84c91c8"
client = Client(account_sid, auth_token)


def SendSMS(numToSend, temp, timeDate,): 

    messageBody = "The temperature is " + str(temp) + " degrees at " + timeDate

    message = client.messages \
                    .create(
                        body=messageBody,
                        from_='+12182506623',
                        to=numToSend
                    )

    print(message.sid)

def SendWeeklyLog(numToSend, timePassed):
    messageBody = "You have spent " + str(timePassed) + " minutes with the lights on this week"
    message = client.messages \
                    .create(
                        body=messageBody,
                        from_='+12182506623',
                        to=numToSend
                    )

    print(message.sid)
    
    




if __name__ == "__main__":
    try:
        SendSMS("+1 438 396 4381", 25, "12:00 Sept 9 2022")
    except:
        print("Error")





