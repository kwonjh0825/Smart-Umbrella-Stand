import RPi.GPIO as GPIO
import sys
import time
import asyncio

from weather.weather import weather_parsing 
from motor.motor import motor
from peltier.peltier import peltier_fan
from liquid_sensor.liquid_sensor import liquid_sensor

WEIGHT = 100

global rain 						   # bring "current raing?" every three hours, yes => 1
global temperature 
global water_height				       # bring temperature every three hours	

global up_down                         # up and down
global blower_peltier_on_off           # 1 when it on
global umbrella_inside_container 

global used_umbrella                   # used umbrella => 1, unused umbrella => 0
global umbrella_start_time 
global umbrella_end_time

global weight

weight = 102

rain = 0
temperature = 0
up_down = 0
blower_peltier_on_off = 0
umbrella_inside_container = 0
used_umbrella = 0
umbrella_start_time = 0
umbrella_end_time = 0

def dryOn():
	global rain 	
	global temperature 

	global up_down                    
	global blower_peltier_on_off      
	global umbrella_inside_container 
	
	global used_umbrella 
	global umbrella_start_time 
	global umbrella_end_time 
	
	global weight
	
	max_time_end = time.time() + (10*1)
	while True:
		time.sleep(0.1) # delay
		print("dry On...")
		if time.time() > max_time_end:
			break
	umbrella_inside_container = 1
	used_umbrella = 0
	umbrella_start_time = 0
	umbrella_end_time = 0
			
def loadCellDetect():
	# reading the weight on the loadCell
    
	global rain 	
	global temperature 

	global up_down                    
	global blower_peltier_on_off      
	global umbrella_inside_container 
	
	global used_umbrella 
	global umbrella_start_time 
	global umbrella_end_time 
	
	global weight
    
	if weight >= WEIGHT:
		if umbrella_end_time - umbrella_start_time <= 30.0: 
			umbrella_start_time = time.time()
			umbrella_inside_container = 1
			used_umbrella = 0
		elif umbrella_end_time - umbrella_start_time >= 30.0:
			umbrella_inside_container = 0
			used_umbrella = 1

		
	else:
		umbrella_end_time = time.time()
		umbrella_inside_container = 1
		used_umbrella = 0
		
	liftUpDown_blowerPeltierOnOff()
				
		
def liftUpDown_blowerPeltierOnOff():
	global rain 	
	global temperature 

	global up_down                    
	global blower_peltier_on_off      
	global umbrella_inside_container 
	
	global used_umbrella 
	global umbrella_start_time 
	global umbrella_end_time 
	
	global weight
	
	# The loadCell detects the weight of the umbrella in real time
	# update variable "used_umbrella"
	
	if umbrella_inside_container == 1:
		if up_down == 0:
			up_down = 1
			# motor(1,1,1, up_down)
		if blower_peltier_on_off == 1:
			blower_peltier_on_off = 0
			# pertier_fen(1,1,1, blower_peltier_on_off)
			
	elif used_umbrella == 1:
		if up_down == 1:
			up_down = 0
			# motor(1,1,1, up_down)
		if blower_peltier_on_off == 0:
			blower_peltier_on_off = 1
			# pertier_fen(1,1,1, blower_peltier_on_off)
		# dryOn()
			
	else:
		if up_down == 0:
			up_down = 1
			# motor(1,1,1, up_down)
		if blower_peltier_on_off == 1:
			blower_peltier_on_off = 0
			# pertier_fen(1,1,1, blower_peltier_on_off)

# weather data reading
async def loadWeather():
	global rain
	global temperature
	while(1):

		rain, temperature = weather_parsing()
		await asyncio.sleep(60 * 60 * 3)
		
async def loadLiquid():
	global water_height
	while(1):
		water_height = liquid_sensor(23)
		await asyncio.sleep(3)

async def core():
	global rain 	
	global temperature 

	global up_down                    
	global blower_peltier_on_off      
	global umbrella_inside_container 
	
	global used_umbrella 
	global umbrella_start_time 
	global umbrella_end_time 
	
	global weight
    

	while(1):
		print("Hello Core")
		if rain == 0:
			if up_down == 1:
				up_down = 0  
				# motor(1,1,1, up_down)
			if blower_peltier_on_off == 1:
				blower_peltier_on_off = 0
				# pertier_fen(1,1,1, blower_peltier_on_off)

		else:
			loadCellDetect()
		await asyncio.sleep(2) # delay


async def main():
	global rain 	
	global temperature
	global water_height

	global up_down                    
	global blower_peltier_on_off      
	global umbrella_inside_container 
	
	global used_umbrella 
	global umbrella_start_time 
	global umbrella_end_time 
	
	global weight
	
	weather  = asyncio.create_task(loadWeather())
	core = asyncio.create_task(core())
	water_high_measure = asyncio.create_task(liquid_sensor())
	
	await asyncio.gather(weather, core, water_high_measure)
	
	
	
if  __name__ == "__main__":
	try :
		asyncio.run(main())
	except KeyboardInterrupt:
		GPIO.cleanup()
		sys.exit(0)
