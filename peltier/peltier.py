import RPi.GPIO as GPIO
import time


def peltier_fan(fan, peltier): 
   #parmeter1=relay_01(Fan), 
   #parmeter2=relay_02(peltier)
    
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(fan, GPIO.OUT)
   GPIO.setup(peltier, GPIO.OUT)  

   print("Peltier, fan on 60s")
   GPIO.output(fan, 0)   # ON
   GPIO.output(peltier, 0) 
   time.sleep(60)

   print("Peltier, fan off")
   GPIO.output(fan, 1)   #OFF
   GPIO.output(peltier, 1)

