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


def getNextDepatureTiming(busStopCode):
    now = datetime.now().replace(year = 2021,month = 5, day = 3,hour = 14, second = 0, microsecond=0)
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
    colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken','day_of_week','minuteOfDay','average_speed', 'distance_to_next', 'too_slow', 'sin_half_hour', 'cos_half_hour', 'month', 'sin_month', 'cos_month']
    df = pd.read_csv ('full_tooSlow.csv', names=colNames, skiprows=1)
    df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
    df.sort_values(by='socket_datetime', inplace = True)

    end = datetime.now().replace(year = 2021,month = 5, day = 3,hour = 14, second = 0, microsecond=0)
    start = end.replace(hour = 0)

    df = df[(df['socket_datetime'] < end) & (df['socket_datetime'] > start)]
    return df.tail(1)

def getCyclicTime(d):
    half_hour = (d.hour * 2) + math.floor(d.minute / 30)
    month = d.month
    sin_half_hour = math.sin(2 * math.pi * half_hour / 48)
    cos_half_hour = math.cos(2 * math.pi * half_hour / 48)
    sin_month = math.sin(2 * math.pi * month /12)
    cos_month = math.cos(2 * math.pi * month /12)
    return sin_half_hour, cos_half_hour, sin_month, cos_month

def getDistanceToNext(busStopCode):
    fKulaiToLarkin = open('KulaiToLarkin.json')
    KulaiToLarkinData = json.load(fKulaiToLarkin)
    fLarkinToKulai = open('LarkinToKulai.json')
    LarkinToKulaiData = json.load(fLarkinToKulai)

    if(busStopCode < 7001):
        return(next(
            (obj['distanceToNext'] for obj in KulaiToLarkinData if obj['code'] == busStopCode),
            None))
    else:
        return(next(
            (obj['distanceToNext'] for obj in LarkinToKulaiData if obj['code'] == busStopCode),
            None))
        
def predict(busStopCode, time):

    scalerX = joblib.load('scalerX.save')
    scalerY = joblib.load('scalerY.save')
    model = keras.models.load_model('model.h5')

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
    
def combinePrediction(busStopCode, predictingBusStop, time):
    total_seconds = 0
    while busStopCode < predictingBusStop:
        seconds = predict(busStopCode, time)
        total_seconds += int(seconds)
        time = time + timedelta(0, int(seconds))
        busStopCode += 1
    return total_seconds, time    

def trackBus(predictingBusStop):
    data = fetchLiveData()
    print(data[['socket_datetime', 'busStop']])
    busStopCode = data['busStop'].item()
    if(busStopCode > predictingBusStop):
        print("get next departure timing")
        nextDepatureTiming = getNextDepatureTiming(predictingBusStop)
        busStopCode = (math.floor(predictingBusStop/1000) * 1000) + 1
        print(nextDepatureTiming, busStopCode)
        total_seconds, time = combinePrediction(busStopCode, predictingBusStop, nextDepatureTiming)
    else:
        print("still behind the bus stop")
        dateString = str(data['socket_datetime'].item())
        socket_datetime = datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
        total_seconds, time = combinePrediction(busStopCode, predictingBusStop, socket_datetime)
        total_seconds -= (datetime.now() - data['socket_datetime']).seconds
    
    return total_seconds, time

app = Flask(__name__)    
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/', methods=['GET'])
@cross_origin()
def welcome():
    args = request.args
    busStopCode = int(args.get('busStop'))
    total_seconds, time = trackBus(busStopCode)
    data = {
        "time" : time,
        "total_seconds": total_seconds
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)