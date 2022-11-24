import RPi.GPIO as GPIO
import time

def peltier_fan(fan, peltier, blower_peltier_on_off): 
   #parmeter1=relay_01(Fan), 
   #parmeter2=relay_02(peltier)
    
   GPIO.setmode(GPIO.BCM) 
   GPIO.setup(fan, GPIO.OUT)
   #GPIO.setup(peltier, GPIO.OUT)  
   if blower_peltier_on_off:
      print("Peltier, fan on")
      GPIO.output(fan, 0)   # ON
      #GPIO.output(peltier, 0) 

   
   else:
      print("Peltier, fan off")
      GPIO.output(fan, 1)   #OFF
      #GPIO.output(peltier, 1)

#peltier_fan(7,23,0)

'''
def peltier_fan(pin, peltier, blower_peltier_on_off): 
   #parmeter1=relay_01(Fan), 
   #parmeter2=relay_02(peltier)
    
   GPIO.setmode(GPIO.BCM) 
   GPIO.setup(pin, GPIO.OUT)
   
   if blower_peltier_on_off:
      print("Peltier, fan on")
      GPIO.output(pin, 0)   # ON
   
   else:
      print("Peltier, fan off")
      GPIO.output(pin, 1)   #OFF

peltier_fan(23,23,1)
'''
