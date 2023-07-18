import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta
import json

fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

def matchToBusStop(lat, lng, direction):
    lat = float(lat)
    lng = float(lng)
    busStopCode = None
    if(direction == 1):
        for point in KulaiToLarkinData:
            if(abs(point['loc'][0] - lat) < 3e-4 and abs(point['loc'][1] - lng) < 3e-4):
                busStopCode = point['code']
                break
    else:
        for point in LarkinToKulaiData:
            if(abs(point['loc'][0] - lat) < 3e-4 and abs(point['loc'][1] - lng) < 3e-4):
                busStopCode = point['code']
                break
    return busStopCode

colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken','day_of_week','minuteOfDay','average_speed', 'distance_to_next', 'too_slow', 'sin_half_hour', 'cos_half_hour', 'month', 'sin_month', 'cos_month']
df = pd.read_csv ('full_tooSlow.csv', names=colNames, skiprows=1)
df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
df.sort_values(by='socket_datetime', inplace = True)

end = datetime.now().replace(year = 2021,month = 5, day = 3, hour=14, second = 0, microsecond=0)
start = end.replace(hour = 0)

df = df[(df['socket_datetime'] < end) & (df['socket_datetime'] > start)]
df = df.tail(1)
dateString = str(df['socket_datetime'].item())
a = datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
print(a)
print(type(a))
a += timedelta(0, 2)
print(a)