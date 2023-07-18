import requests
import json
from datetime import datetime, timedelta
import math

fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

def matchToBusStop(lat, lng):
    print(lat,lng)
    lat = float(lat)
    lng = float(lng)
    busStopCode = None
    for point in KulaiToLarkinData:
        if(abs(point['loc'][0] - lat) < 3e-4 and abs(point['loc'][1] - lng) < 3e-4):
            busStopCode = point['code']
 
    for point in LarkinToKulaiData:
        if(abs(point['loc'][0] - lat) < 3e-4 and abs(point['loc'][1] - lng) < 3e-4):
            busStopCode = point['code']

    print(busStopCode)


def call():
    dateToday = datetime.today()
    print(dateToday)
    url = 'https://dataapi.paj.com.my/api/v1/bus-live/bus/JSJ7542/'
    # dateToday = '2023-07-12'
    # url = 'https://dataapi.paj.com.my/api/v1/bus-history/JSJ7542/' + dateToday

    api_key = '8923a80ca7164210b07f92c4f47268f1'
    headers = {'api-key': api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()['data']
        matchToBusStop(data[0]['latitude'], data[0]['longitude'])
        return data
    else:
        print('Error:', response.status_code)

def abc():
    for i in range(3):
        data = call()
        print(data)

abc()


