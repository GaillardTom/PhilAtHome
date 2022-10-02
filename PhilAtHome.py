from SendSMS import SendSMS
import RPi.GPIO as GPIO
import time
import os
import datetime
import math
from Database import FetchData

import ADC0832
from datetime import date

# ENVIRONMENT VARIABLES
CLIENT_PHONE = os.environ.get("CLIENT_PHONE")

# DECLARE PIN NUMBERS HERE

LEDPIN = 12
TRIG = 23
ECHO = 24
DIO = 27  # board 13
CLK = 18  # board 12
STB = 17  # board 11
LSBFIRST = 0
MSBFIRST = 1

# Global variable that are not pin numbers

temperature = 0  # declare temperature variable
format = "%H:%M:%S"
formatDay = "%d-%m-%Y"


# SETUP GPIO
def SetupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDPIN, GPIO.IN)
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(LEDPIN, GPIO.OUT)  # set the red light as output
    ADC0832.setup()
    TM1638_init()


def turnOnRedLight():

    GPIO.output(LEDPIN, GPIO.LOW)  # turn on red light


def readSensorForTemperature(id):
    tfile = open("/sys/bus/w1/devices/"+id+"/w1_slave")  # open the sensor file

    text = tfile.read()  # read the text file

    tfile.close()  # close the file

    secondline = text.split("\n")[1]  # get the second line of the file

    temperaturedata = secondline.split(" ")[9]  # get the temperature data

    # get the temperature from the sensor
    temperature = float(temperaturedata[2:])

    temperature = temperature / 1000  # convert the temperature to celsius
    print("Sensor: " + id + " . Current temperature: %0.3f (" % temperature)

    temperature = "%0.3f" % temperature  # format the temperature to 3 decimal places

    return temperature  # return the temperature


def Temperature():

    try:
        global temperature
        count = 0
        sensor = ""
        for file in os.listdir("/sys/bus/w1/devices"):
            if file.startswith("28-"):
                count = count + 1  # increment the count by 1
                # read the temperature of the sensor
                temp = readSensorForTemperature(file)
                time.sleep(1)  # wait for 1 second
                return temp  # return the temperature
        if (count == 0):
            print("No sensors found")  # Display that there is no sensor found
    except KeyboardInterrupt:
        destroy()

######################################

    # SETUP SEVEN SEGMENT DISPLAY


######################################


def _shiftOut(dataPin, clockPin, bitOrder, val):
    for i in range(8):
        if bitOrder == LSBFIRST:
            GPIO.output(dataPin, val & (1 << i))
        else:
            GPIO.output(dataPin, val & (1 << (7 - i)))
        GPIO.output(clockPin, True)
        time.sleep(0.000001)
        GPIO.output(clockPin, False)
        time.sleep(0.000001)


def bitRead(value, bit):
    return value & (1 << bit)


def pickDigit(digit):
    print('test')


def sendCommand(cmd):
    GPIO.output(STB, False)
    _shiftOut(DIO, CLK, LSBFIRST, cmd)
    GPIO.output(STB, True)


def TM1638_init():
    GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DIO, GPIO.OUT)
    GPIO.setup(CLK, GPIO.OUT)
    GPIO.setup(STB, GPIO.OUT)
    sendCommand(0x8f)


def GetIntpart(num):
    _, firstNum = math.modf(num/1000 % 10)
    _, secNum = math.modf(num/100 % 10)
    _, thirdNum = math.modf(num/10 % 10)
    _, fourthNum = math.modf(num % 10)
    return int(firstNum), int(secNum), int(thirdNum), int(fourthNum)


def numberDisplay(num):
    digits = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]
    sendCommand(0x40)
    firstNum, secNum, thirdNum, fourthNum = GetIntpart(num)
    # Display the number onto the seven segment display
    GPIO.output(STB, False)
    _shiftOut(DIO, CLK, LSBFIRST, 0xc0)
    _shiftOut(DIO, CLK, LSBFIRST, digits[firstNum])
    _shiftOut(DIO, CLK, LSBFIRST, 0x00)
    _shiftOut(DIO, CLK, LSBFIRST, digits[secNum])
    _shiftOut(DIO, CLK, LSBFIRST, 0x00)
    _shiftOut(DIO, CLK, LSBFIRST, digits[thirdNum])
    _shiftOut(DIO, CLK, LSBFIRST, 0x00)
    _shiftOut(DIO, CLK, LSBFIRST, digits[fourthNum])
    _shiftOut(DIO, CLK, LSBFIRST, 0x00)
    GPIO.output(STB, True)


def photoresistor():
    timerStart = None
    # global light  # put the variable light as global to be changed by the method
    light = ADC0832.getResult()  # read the light sensor
    time.sleep(1)  # wait for 1 second
    # print("Light: " + str(light))  # print the light sensor
    print("light status", light)
    if light >= 40:
        timerStart = datetime.datetime.utcnow(
        ) - datetime.timedelta(hours=4)  # get the current time
        dayStart = date.today()  # get the current day
        GPIO.output(LEDPIN, GPIO.HIGH)
    else:

        turnOnRedLight()  # turn on red light

        if (timerStart != None):
            timerEnd = datetime.datetime.now().strftime(format)  # get the current time
            dayFinish = date.today()  # get the current day

            if (dayStart == dayFinish):
                lightTimeForDay = timerEnd - timerStart  # get the time the light was on for
                # Call the write to file function to write the data to the file
                WriteToFile(dayStart, lightTimeForDay)


# TODO - ADD DISTANCE SENSOR AND SEND SMS WHEN DISTANCE IS LESS THAN 10CM
def distanceSensor():
    print("Distance Sensor")
    GPIO.output(TRIG, False)
    print("Waiting For Sensor To Settle")
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    #time.sleep(0.01)
    pulse_start = None
    start_time = time.time() 
    while GPIO.input(ECHO) == 0:
        print("Starting pulse")
        
        pulse_start = time.time()
        if pulse_start - start_time >= 5: 
            GPIO.output(TRIG, False)
            print("Waiting For Sensor To Settle")
            time.sleep(2)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            #time.sleep(0.01)
            pulse_start = None
            start_time = time.time() 
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print("Distance:", distance, "cm")
    return distance


def WriteToFile(day, lightTimeForDay):
    # Open the file in append & read mode ('a+')
    f = open("/data/lightTime.txt", "a")
    # Write text to file day + time of light turned on
    f.write(day + " " + lightTimeForDay + "\n")
    # Close the file
    f.close()


def destroy():
    # GPIO.output(LEDPIN, GPIO.LOW)  # turn off led
    ADC0832.destroy()

    GPIO.cleanup()  # Release resource
    exit(1)


# MAIN LOOP FUNCTION
def main():
    print("I love Sach")
    while True:
        try:
            temp = Temperature()
            print(temp)
            numberDisplay(float(temp))
            distance = distanceSensor()
            photoresistor()
            if distance < 10:
                timeOfDay = datetime.datetime.utcnow(
                ) - datetime.timedelta(hours=4)  # get the current time
                dateResult = date.today()
                resultDateTime = str(timeOfDay)
                SendSMS(CLIENT_PHONE, temp,  resultDateTime)
            else:
                print("No SMS sent")
        except:
            timeOfDay = datetime.datetime.utcnow(
            ) - datetime.timedelta(hours=4)  # get the current time
            dateResult = date.today()  # Get the current date
            resultDateTime = str(timeOfDay)
            print("Error contacting user ...")
            SendSMS(CLIENT_PHONE, temp,  resultDateTime, error=True)
            time.sleep(1)
            destroy()


if __name__ == "__main__":
    try:
        SetupGPIO()
        while True:
            main()
    except (KeyboardInterrupt):
        print("Exit Program")
