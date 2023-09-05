import requests
import json
from datetime import datetime, timedelta
from flask import Flask,jsonify, request
from flask_cors import CORS, cross_origin
import threading

import numpy as np
import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

# importing the libraries
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from sklearn import metrics
from sklearn import preprocessing
import joblib

fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

scalerX = joblib.load('scalerX.save')
scalerY = joblib.load('scalerY.save')
model = keras.models.load_model('model.h5')


lastBusStopCode = None
lastBusStopTime = None

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

def getNextDepatureTiming(busStopCode):
    now = datetime.now()
    minuteOfDay = now.hour * 60 + now.minute
    if(busStopCode < 7001):
        if(minuteOfDay < 540):
            return(now.replace(hour = 9, minute = 0, second = 0, microsecond=0))
        elif(minuteOfDay < 720):
            return(now.replace(hour = 12, minute = 0, second = 0, microsecond=0))
        elif(minuteOfDay < 870):
            return(now.replace(hour = 14, minute = 30, second = 0, microsecond=0))
        elif(minuteOfDay < 1020):
            return(now.replace(hour = 17, minute = 0, second = 0, microsecond=0))
        else:
            return(now.replace(hour = 6, minute = 0, second = 0, microsecond=0) + timedelta(days=1))
    else:
        if(minuteOfDay < 615):
            return(now.replace(hour = 9, minute = 0, second = 0, microsecond=0))
        elif(minuteOfDay < 795):
            return(now.replace(hour = 12, minute = 0, second = 0, microsecond=0))
        elif(minuteOfDay < 945):
            return(now.replace(hour = 14, minute = 30, second = 0, microsecond=0))
        elif(minuteOfDay < 1095):
            return(now.replace(hour = 17, minute = 0, second = 0, microsecond=0))
        else:
            return(now.replace(hour = 7, minute = 15, second = 0, microsecond=0) + timedelta(days=1))

    
def fetchLiveData():
    api_key = '8923a80ca7164210b07f92c4f47268f1'
    headers = {'api-key': api_key}
    url = 'https://dataapi.paj.com.my/api/v1/bus-live/bus/JSJ7542/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return(response.json()['data'])
    else:
        print('Error:', response.status_code)

def getCyclicTime(d):
    half_hour = (d.hour * 2) + math.floor(d.minute / 30)
    month = d.month
    sin_half_hour = math.sin(2 * math.pi * half_hour / 48)
    cos_half_hour = math.cos(2 * math.pi * half_hour / 48)
    sin_month = math.sin(2 * math.pi * month /12)
    cos_month = math.cos(2 * math.pi * month /12)
    return sin_half_hour, cos_half_hour, sin_month, cos_month

def getDistanceToNext(busStopCode):
    if(busStopCode < 7001):
        return(next(
            (obj['distanceToNext'] for obj in KulaiToLarkinData if obj['code'] == busStopCode),
            None))
    else:
        return(next(
            (obj['distanceToNext'] for obj in LarkinToKulaiData if obj['code'] == busStopCode),
            None))
        
def predict(busStopCode, time):
    sin_half_hour, cos_half_hour, sin_month, cos_month = getCyclicTime(time)
    distanceToNext = getDistanceToNext(busStopCode)
    x = [sin_half_hour, cos_half_hour, sin_month, cos_month, distanceToNext]
    for i in range(6001, 6032):
        if(i != busStopCode):
            x.append(0)
        else:
            x.append(1)
    for i in range (7001, 7036):
        if(i != busStopCode):
            x.append(0)
        else:
            x.append(1)
    for i in [60141, 60161, 60301]:
        if(i != busStopCode):
            x.append(0)
        else:
            x.append(1)

    X_scaled = scalerX.transform([x])
    y_pred_scaled = model.predict(X_scaled)
    y_pred = scalerY.inverse_transform(y_pred_scaled)[0][0]
    return y_pred
    
def combinePrediction(start, end, time):
    total_seconds = 0
    while start < end:
        seconds = predict(start, time)
        total_seconds += seconds
        time = time + timedelta(0, seconds)
        start += 1
    return total_seconds, time

def getTimeOfArrival(busStopCode):
    if(lastBusStopCode):
        passed = False
        if((lastBusStopCode < 7001 and busStopCode < 7001) or (lastBusStopCode >= 7001 and busStopCode >=7001)):
            if(lastBusStopCode >= busStopCode):
                passed = True
        else:
            passed = True
        if(passed):
            time_travelled = datetime.now() - lastBusStopTime
            seconds_travelled = time_travelled.seconds
            if(lastBusStopCode < 7001):
                total_seconds, time = combinePrediction(6001, busStopCode, getNextDepatureTiming)
            else:
                total_seconds, time = combinePrediction(7001, busStopCode, getNextDepatureTiming)
        else:
            total_seconds, time = combinePrediction(lastBusStopCode, busStopCode, lastBusStopTime)
            total_seconds -= seconds_travelled
            time -= time_travelled
    else:
        total_seconds = 0
        time = 0
    return(total_seconds, time)
    

def trackBus():
    threading.Timer(10, trackBus).start()
    data = fetchLiveData()
    direction = getDirection()
    busStopCode = matchToBusStop(data[0]['latitude'], data[0]['longitude'], direction)
    if(busStopCode):
        global lastBusStopCode
        global lastBusStopTime
        lastBusStopCode = int(busStopCode)
        lastBusStopTime = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')


app = Flask(__name__)    
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/', methods=['GET'])
@cross_origin()
def welcome():
    args = request.args
    busStopCode = int(args.get('busStop'))
    total_seconds, time = getTimeOfArrival(busStopCode)
    data = {
        "time" : time,
        "total_seconds": total_seconds
    }
    return jsonify(data)

if __name__ == '__main__':
    trackBus()
    app.run(host='0.0.0.0', port=105)