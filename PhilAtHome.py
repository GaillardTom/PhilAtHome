from SendSMS import SendSMS
import RPi.GPIO as GPIO 
import ADC0832

# DECLARE PIN NUMBERS HERE 

LEDPIN = 3 







#SETUP GPIO 
def SetupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDPIN, GPIO.IN)
    ADC0832.setup()


# MAIN LOOP FUNCTION
def main():
    print("I love Sach")


def destroy():
    GPIO.cleanup()
    ADC0832.destroy()


if __name__ == "__main__":
    try:
        SetupGPIO()
        while True: 
            main()
    except (KeyboardInterrupt):
        print("Exit Program")
        destroy()