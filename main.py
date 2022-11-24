import RPi.GPIO as GPIO
import sys
import time
import asyncio
import json
import requests

from weather.weather import weather_parsing 
from motor.motor import motor
from peltier.peltier import peltier_fan
from liquid_sensor.liquid_sensor import liquid_sensor
from loadCell.hx711 import HX711


WEIGHT = 500

global rain 				# bring "current raing?" every three hours, yes => 1
global temperature 
global water_height			# bring temperature every three hours	

global up_down                          # up and down
global blower_peltier_on_off            # 1 when it on
global umbrella_inside_container 

global used_umbrella                    # used umbrella => 1, unused umbrella => 0
global umbrella_start_time 
global umbrella_end_time

global weight
global url

weight = 102
url = 'http://127.0.0.1:5000/state_ajax'

rain = 0
temperature = 0
up_down = 0
blower_peltier_on_off = 0
umbrella_inside_container = 0
used_umbrella = 0
umbrella_start_time = 0
umbrella_end_time = 0

fan_pin = 7			# physical 26
peltier_pin = 23	# physical 16

ENA_pin = 17	# physical 11
IN1_pin = 27	# physical 13
IN2_pin = 22	# physical 15

loadCell_pin1 = 6 # physical 31
loadCell_pin2 = 13 # physical 33


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
		time.sleep(0.1) # del
		print("dry On...")
		if time.time() > max_time_end:
			break
	umbrella_inside_container = 1
	used_umbrella = 0
	umbrella_start_time = 0
	umbrella_end_time = 0
			
def loadCellDetect():
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
		print("Umb is in bucket!!")
		if umbrella_start_time == 0 :
			umbrella_end_time = 0
		if umbrella_end_time - umbrella_start_time <= 10.0: 
			print('!!NoNoNo!!')
			umbrella_start_time = time.time()
			umbrella_end_time = 0
			umbrella_inside_container = 1
			used_umbrella = 0
		elif umbrella_end_time - umbrella_start_time >= 10.0:
			print('YesYesYes')
			umbrella_inside_container = 0
			used_umbrella = 1

		
	else:
		umbrella_end_time = time.time()
		umbrella_inside_container = 2
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
	global url
	
	# The loadCell detects the weight of the umbrella in real time
	# update variable "used_umbrella"
	
	if umbrella_inside_container != 0:
		if blower_peltier_on_off == 1:
			blower_peltier_on_off = 0
			peltier_fan(fan_pin, peltier_pin, blower_peltier_on_off)
		if up_down == 0:
			up_down = 1
			motor(ENA_pin, IN1_pin, IN2_pin, up_down)
			
		#if umbrella_inside_container == 1, state1.html
		if umbrella_inside_container == 1:
			datas = { 'state' : 'state1' }
			response = requests.get(url, params=datas)
		#if umbrella_inside_container == 2, state3.html	
		else:
			datas = { 'state' : 'state3' }
			response = requests.get(url, params=datas)
				
			
			
			
	elif used_umbrella == 1:
		if up_down == 1:
			up_down = 0
			motor(ENA_pin, IN1_pin, IN2_pin, up_down)
		if blower_peltier_on_off == 0:
			blower_peltier_on_off = 1
			peltier_fan(fan_pin, peltier_pin, blower_peltier_on_off)
			
		datas = { 'state' : 'state2' }
		response = requests.get(url, params=datas)
		dryOn()
			
	else:
		if up_down == 0:
			up_down = 1
			motor(ENA_pin, IN1_pin, IN2_pin, up_down)
		if blower_peltier_on_off == 1:
			blower_peltier_on_off = 0
			peltier_fan(fan_pin, peltier_pin, blower_peltier_on_off)
		
		datas = { 'state' : 'state1' }
		response = requests.get(url, params=datas)

# weather data reading
async def loadWeather():
	global rain
	global temperature
	# while(1):
	# 	rain, temperature = weather_parsing()
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
    
	GPIO.setmode(GPIO.BCM)


	referenceUnit = 246
	hx = HX711(loadCell_pin1, loadCell_pin2) # Physical pin => 32, 22

	hx.set_reading_format("MSB", "MSB")

	hx.set_reference_unit(referenceUnit)

	hx.reset()

	hx.tare()

    
	while(1):
		print("Hello Core: Current  Weather", rain)
		if rain == 1:
			if up_down == 1:
				up_down = 0  
				motor(ENA_pin, IN1_pin, IN2_pin, up_down)
			if blower_peltier_on_off == 1:
				blower_peltier_on_off = 0
				peltier_fan(fan_pin, peltier_pin, blower_peltier_on_off)
			datas = { 'state' : 'state0' }
			response = requests.get(url, params=datas)

		else:
			val = hx.get_weight(5)
			print(abs(int(val)))
			hx.power_down()
			hx.power_up()
			time.sleep(0.1)
			
			weight = abs(int(val))
			loadCellDetect()
		await asyncio.sleep(0.5) # delay


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
	
	weather_task = asyncio.create_task(loadWeather())
	core_task = asyncio.create_task(core())
	water_high_measure_task = asyncio.create_task(loadLiquid())
	
	await asyncio.gather(weather_task, core_task, water_high_measure_task)
	
	
	
if  __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		GPIO.cleanup()
		sys.exit(0)
