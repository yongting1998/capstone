import requests
import json
from datetime import datetime
from flask import Flask,jsonify
from flask_cors import CORS, cross_origin

fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

def matchToBusStop(latlng, direction):
    lat, lng = latlng.split(',')
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

# def checkLastBusStop():
#     busHistory = fetchLiveData()
#     currentBusStop = None
#     busStopCodeList = []
#     counter = 0
#     for bus in reversed(busHistory):
#         busStopCode = matchToBusStop(bus['latlng'])
#         if(busStopCode and busStopCode != currentBusStop):
#             busStopCodeList.append(busStopCode)
#             counter += 1
#             if counter == 2:
#                 break
#             currentBusStop = busStopCode
#     print(busStopCodeList)

def getDirection():
    now = datetime.now()
    minuteOfDay = now.hour * 60 + now.minute
    if(minuteOfDay < 435):
        return 1
    if(minuteOfDay < 540):
        return 2
    if(minuteOfDay < 615):
        return 1
    if(minuteOfDay < 720):
        return 2
    if(minuteOfDay < 795):
        return 1
    if(minuteOfDay < 870):
        return 2
    if(minuteOfDay < 945):
        return 1
    if(minuteOfDay < 1020):
        return 2
    if(minuteOfDay < 1095):
        return 1
    else:
        return 2

def fetchLiveData():
    # dateToday = datetime.today().strftime('%Y-%m-%d')
    # url = 'https://dataapi.paj.com.my/api/v1/bus-live/bus/JSJ7542/'
    dateToday = '2023-07-12'

    api_key = '8923a80ca7164210b07f92c4f47268f1'
    headers = {'api-key': api_key}
    url = 'https://dataapi.paj.com.my/api/v1/bus-history/JSJ7542/' + dateToday
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return(response.json()['data'])
    else:
        print('Error:', response.status_code)


def checkLastBusStop():
    direction = getDirection()
    busHistory = fetchLiveData()
    lastBusStop = None
    for bus in reversed(busHistory):
        busStopCode = matchToBusStop(bus['latlng'], direction)
        if(busStopCode):
            lastBusStop = busStopCode
            break
    print(lastBusStop)

app = Flask(__name__)    
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/', methods=['GET'])
@cross_origin()
def welcome():
    data = {
        "time" : 15,
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)