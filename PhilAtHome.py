from SendSMS import SendSMS
import RPi.GPIO as GPIO 
import time
import os
from datetime import datetime



# ENVIRONMENT VARIABLES
PASSWORD = os.environ.get("PASSWORD")

# DECLARE PIN NUMBERS HERE 

LEDPIN = 3 
LIGHTPIN = 4


# Global variable that are not pin numbers

temperature = 0 # declare temperature variable
format = "%H:%M:%S"
formatDay = "%d-%m-%Y"



#SETUP GPIO 
def SetupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDPIN, GPIO.IN)



def turnOnRedLight():
    
    GPIO.setup(LEDPIN, GPIO.OUT)  # set the red light as output
    GPIO.output(LEDPIN, GPIO.HIGH)  # turn on red light
    

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
    while True:
        global temperature
        count = 0
        sensor = ""
        for file in os.listdir("/sys/bus/w1/devices"):
            if file.startswith("28-"):
                count = count + 1  # increment the count by 1
                temp = readSensorForTemperature(file)  # read the temperature of the sensor
                time.sleep(1)  # wait for 1 second
                return temp  # return the temperature
        if (count == 0):
            print("No sensors found") # Display that there is no sensor found
   
   
######################################


    # SETUP SEVEN SEGMENT DISPLAY


######################################


def _shiftOut(dataPin, clockPin, bitOrder, val):
    for i in range(8):
        if bitOrder == LSBFIRST:
            GPIO.output(dataPin, val & (1 << i))
        else:
            GPIO.output(dataPin, val & (1 << (7 -i)))
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
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DIO, GPIO.OUT)
    GPIO.setup(CLK, GPIO.OUT)
    GPIO.setup(STB, GPIO.OUT)
    sendCommand(0x8f)

def numberDisplay(num):
    digits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
    sendCommand(0x40)
    firstNum = int(num/1000%10)
    secNum = int(num/100 % 10)
    thirdNum = int(num/10% 10)
    fourthNum = int(num%10)   
         

    
    
         
            
def photoresistor():
    
    while True:
       
        global light  # put the variable light as global to be changed by the method
        GPIO.setup(LIGHTPIN, GPIO.IN)  # set the light as input
        light = GPIO.input(LIGHTPIN)  # read the light sensor
        time.sleep(1)  # wait for 1 second
        #print("Light: " + str(light))  # print the light sensor
        
        if light == 1:
            timerStart = datetime.now().strftime(format) # get the current time
            dayStart = datetime.now().strftime(formatDay) # get the current day
        else:
            
            turnOnRedLight() # turn on red light 
            
            if (timerStart != None):
                timerEnd = datetime.now().strftime(format) # get the current time
                dayFinish = datetime.now().strftime(formatDay) # get the current day
                
                if (dayStart == dayFinish):
                    lightTimeForDay = timerEnd - timerStart # get the time the light was on for
                    WriteToFile(dayStart, lightTimeForDay) # Call the write to file function to write the data to the file
                
def WriteToFile(day, lightTimeForDay):
    # Open the file in append & read mode ('a+')
    f = open("lightTime.txt", "a")
    # Write text to file day + time of light turned on
    f.write(day + " " + lightTimeForDay + "\n")
    # Close the file
    f.close()
                       
        
def destroy():

    GPIO.output(LEDPIN, GPIO.HIGH)  # turn off led
    GPIO.cleanup() # Release resource


# MAIN LOOP FUNCTION
def main():
    print("I love Sach")





if __name__ == "__main__":
    try:
        SetupGPIO()
        while True: 
            main()
    except (KeyboardInterrupt):
        print("Exit Program")