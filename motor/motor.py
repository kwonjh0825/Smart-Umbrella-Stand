import RPi.GPIO as GPIO
import time

def motor (ENA, IN1, IN2, up_down):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENA, GPIO.OUT)       
    GPIO.setup(IN1, GPIO.OUT)       
    GPIO.setup(IN2, GPIO.OUT)      

    if up_down == 1:
        GPIO.output(IN1, False)     # forward
        GPIO.output(IN2, True)    
        GPIO.output(ENA, True)  
        print("motor going forward")
        time.sleep(3)            

                
        GPIO.output(ENA, False)     # stop
        time.sleep(1)          
    else:
        GPIO.output(IN1, True)      # backward
        GPIO.output(IN2, False)   
        GPIO.output(ENA, True)
        print("motor going backward")  
        time.sleep(10)               
                
        GPIO.output(ENA, False)     # stop
        time.sleep(1)              

#motor(17,27,22,1)
