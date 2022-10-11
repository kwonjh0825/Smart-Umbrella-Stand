import requests
import datetime
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

rain = 0
temperature = 0


def weather_parsing():  
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"     # url for requesting data
    service_key = os.environ.get('SERVICE_KEY')         # get key from dotenv

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
    return rain, temperature
