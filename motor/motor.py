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
        print("motor is up")
        time.sleep(2)            

                
        GPIO.output(ENA, False)     # stop        
    else:
        GPIO.output(IN1, True)      # backward
        GPIO.output(IN2, False)   
        GPIO.output(ENA, True)
        print("motor is down")  
        time.sleep(2)               
                
        GPIO.output(ENA, False)     # stop             

#motor(17,27,22,0)
