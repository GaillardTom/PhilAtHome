# PhilAtHome
Tom and Sacha MidTerm IOT project built on Python, using the Twilio communication API and connected to a MongoDB database.

## Goal of this project
Make an application that detects light, temperature and movement using the Raspberry Pi and the Adeept sensor kit. Whenever light is detected, a timer will start to calculate the number of time that the light was on and when light is not detected, a LED will illuminate to show the light switch. At the end of everyday, a report of the time that the lights were on will be inserted in the MongoDB. Whenever movement is detected, a SMS containing the time of the day, the date and the temperature will be sent to the user. This application runs as a service and contains two cron jobs, one for a daily insert to the database and one for a weekly report of the total number of time the lights were on that will be sent to the user in a SMS.

## Setup for project
- **Have a [Twilio](https://www.twilio.com/) account**
- **Have a [MongoDB](https://www.mongodb.com/) instance on your machine**
-  **Raspberry Pi**
- **Ultrasonic distance sensor**
- **4-digit 7 segment display**
- **DS18b20 temperature sensor**
- **One LED**
- **ADC0832**
- **Breadboard**
- [**Extension board GPIO**](https://www.adeept.com/gpio-extension_p0105.html)
## Setup of your Raspberry Pi Breadboard

****
**The pin numbers are in BCM mode ex: GPIO 23**
****
- **Ultrasonic distance [sensor](https://www.adeept.com/ultrasonic-sr04_p0047.html)**, 
>Trig pin on GPIO 23
****
>Echo pin on GPIO 24
****
- **4-digit 7 segment [display](https://www.adeept.com/tm1638-segment_p0055.html)**
>Diop pin on GPIO 27
****
>Clk pin on GPIO 18
****
>Stb pin on GPIO 17
****
- **DS18b20 temperature [sensor](https://www.adeept.com/ds18b20_p0064.html)**
> You can use [this](https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/) guide and follow the ENABLE THE ONE-WIRE INTERFACE section to setup your temperature sensor
****
- **LED**
> On GPIO 12
****
- **[ADC0832](https://www.adeept.com/adc0832_p0131.html)**
> DIO pin on GPIO 25
****
> CS pin on GPIO 5
****
> CLK pin on GPIO 6
****
- **Photoresistor**

## Setting up your Twilio account 
> Go to [this](https://www.twilio.com/) website
****
> Click on **Sign up**
****
> Create an account
****
> Setup an active phone number with your Twilio account
****
> Copy the **Account SID** and the **Auth Token** under the **Account Info** tab
**** 
> Put them both in your .env file in their respective variables
****
### Help: [Twilio Documentation](https://www.twilio.com/docs/sms/send-messages)
****
## Content of your .env file
- account_sid=**[YOUR TWILIO ACCOUNT SID]**
- CLIENT_PHONE=**[YOUR PHONE NUMBER ex: +11234567890]**
- auth_token=**[YOUR TWILIO AUTHENTICATION TOKEN]**
- DBSTRING=**[CONNECTION STRING TO YOUR MONGODB]**

## Setting up the cron jobs
This project has 2 cron jobs, a weekly report and a daily insert to the database
> Open your terminal
****
> cd into PhilAtHome directory
****
> Enter **sudo chmod +x \*.py** to make all the python scripts executable
****
> Enter **which python3** and copy the output
****
> Enter **crontab -e** in your terminal
****
> At the bottom of the file, write 
>>- SHELL=/bin/bash
>>- DBSTRING=[**CONNECTION STRING TO YOUR MONGODB**]
>>- account_sid=[**YOUR TWILIO ACCOUNT SID**]
>>- CLIENT_PHONE=[**YOUR PHONE NUMBER ex: +11234567890**]
>>- auth_token=[**YOUR TWILIO AUTHENTICATION TOKEN**]
****
### For the weekly report
****
> Under what you just wrote, add this **59 23 * * 0 [The output of the which python3 command] [Path/to/WeeklyReportPhilAtHome.py]**
### For the daily report
****
> Add this **59 23 * *  * [The output of the which python3 command] [Path/to/DailyLogging.py]** (Do not remove the weekly cron job that you just entered)
