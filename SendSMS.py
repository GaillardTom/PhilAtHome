
import os
from twilio.rest import Client


# Send a SMS with the twillio API using python3


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
client = Client(account_sid, auth_token)


def SendSMS(numToSend, temp, timeDate, error=False): 
    if error:
        messageBody = "Error: Please restart the service or contact an admin DATETIME: " + timeDate
    else:
        messageBody = "The temperature is " + \
            str(temp) + " degrees at " + timeDate
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
    
    


    print(message.sid)


if __name__ == "__main__":
    try:
        SendSMS("+1 438 396 4381", 25, "12:00 Sept 9 2022")
    except:
        print("Error")
