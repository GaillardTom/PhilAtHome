from SendSMS import SendSMS
import RPi.GPIO as GPIO 


# DECLARE PIN NUMBERS HERE 

LEDPIN = 3 







#SETUP GPIO 
def SetupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDPIN, GPIO.IN)


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