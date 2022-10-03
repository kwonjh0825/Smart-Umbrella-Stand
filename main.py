import math 
import time
import requests
# import datetime
# from datetime import date, datetime, timedelta
# from dotenv import load_dotenv
# import os

# load_dotenv()

WEIGHT = 100

global rain 						   # bring "current raing?" every three hours, yes => 1
global temperature 				       # bring temperature every three hours	

global up_down                         # up and down
global blower_peltier_on_off           # 1 when it on
global umbrella_inside_container 

global used_umbrella                   # used umbrella => 1, unused umbrella => 0
global umbrella_start_time 
global umbrella_end_time

rain = 0
temperature = 0
up_down = 0
blower_peltier_on_off = 0
umbrella_inside_container = 0
used_umbrella = 0
umbrella_start_time = 0
umbrella_end_time = 0


'''
def weather_parsing():  
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"     # url for requesting data
    service_key = os.environ.get('SERVICE_KEY')         # get key from dotenv
    
    global rain                                         # 0 means clear
    global temperature

    rain = 0
    temperature = 0

    today = datetime.today()
    today_date =  today.strftime("%Y%m%d")              # ex) 20220527
    base_date = today_date                              # basedate is today
    yesterday_date = date.today() - timedelta(days=1)   # this is needed when the time is 00:00 ~ 02:10
    time = datetime.now()
    
    # set basetime by clock
    
    if  time.hour < 2 or (time.hour == 2 and time.minute <= 10):        # 00:00 ~ 02:10
        base_date = yesterday_date                                      # base_date, time : yesterday 23:00
        base_time = "2300"
    elif time.hour < 5 or (time.hour == 5 and time.minute <= 10):       # 02:11 ~ 05:10
        base_time = "0200"
    elif time.hour<8 or (time.hour == 8 and time.minute <= 10):         # 05:11 ~ 08:10
        base_time = "0500"
    elif time.hour <= 11 or (time.hour == 11 and time.minute <= 10):    # 08:11 ~ 11:10
        base_time = "0800"
    elif time.hour < 14 or (time.hour == 14 and time.minute <= 10):     # 11:11 ~ 14:10
        base_time = "1100"
    elif time.hour < 17 or (time.hour == 17 and time.minute <= 10):     # 14:11 ~ 17:10
        base_time = "1400"
    elif time.hour < 20 or (time.hour == 20 and time.minute <= 10):     # 17:11 ~ 20:10
        base_time = "1700" 
    elif time.hour < 23 or (time.hour == 23 and time.minute <= 10):     # 20:11 ~ 23:10
        base_time = "2000"
    else:                                                               # 23:11 ~ 23:59
        base_time = "2300"
    
    # set nx, ny ( daeyeon )
    nx = "98"
    ny = "75"

    payload = f"serviceKey={service_key}&dataType=json&base_date={base_date}&" +\
        f"base_time={base_time}&nx={nx}&ny={ny}"

    res = requests.get(weather_url + payload)                           # request data 
    items = res.json().get('response').get('body').get('items')         # getting data
    
    for item in items['item']:
        # temperature
        if item['category'] == 'TMP':
            temperature = item['fcstValue']
        
        # condition
        if item['category'] == 'PTY':
            weather_code = item['fcstValue']
            if weather_code == '0':
                rain = 0                            #clear
            else:
                rain = 1                            #rain
    return 0
'''
flags = 0

def loadCellDetect():
    # reading the weight on the loadCell
    
    
    if weight >= WEIGHT:
		if umbrella_end_time - umbrella_start_time <= 30.0: 
			umbrella_start_time = time.time()
			umbrella_inside_container = 1
			used_umbrella = 0
		elif umbrella_end_time - umbrella_start_time >= 30.0:
			umbrella_inside_container = 0
			used_umbrella = 1
			 
			''' 60 sec -> loadCel Function not working
			liftUpDown_blowerPeltierOnOff()
			'''
			
			umbrella_inside_container = 1
			used_umbrella = 0
			umbrella_start_time = 0
			umbrella_end_time = 0
		
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
	
	# The loadCell detects the weight of the umbrella in real time
	# update variable "used_umbrella"
	
	if rain == 0:
		if up_down == 1:
			up_down = 0  
		if blower_peltier_on_off == 1:
			blower_peltier_on_off = 0
	elif umbrella_inside_container == 1:
		if up_down == 0:
			up_down = 1
		if blower_peltier_on_off == 1:
			blower_peltier_on_off = 0
	elif used_umbrella == 1:
		if up_down == 1:
			up_down = 0
		if blower_peltier_on_off == 0:
			blower_peltier_on_off = 1
	else:
		if up_down == 0:
			up_down = 1
		if blower_peltier_on_off == 1:
			blower_peltier_on_off = 0
		
			
while True:
	time.sleep(0.1) # delay
	if rain == 0:
		if up_down == 1:
			up_down = 0  
		if blower_peltier_on_off == 1:
			blower_peltier_on_off = 0
		
	else:
		loadCellDetect()

