import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
import math
from datetime import date

fKulaiToLarkin = open('../../dataset/KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('../../dataset/LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

def onRoute():
    dataNames=['202203']
    colNames=['a','b','id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

    for x in dataNames:
        df = pd.read_csv ('../../dataset/dataset_direction/' + x + '_direction.csv', names=colNames, skiprows=1)
        df = df.drop(['a', 'b'], axis=1)
        df['lat'] = df['lat'].astype(float)
        df['long'] = df['long'].astype(float)
        #df = df [600000:]
        df = df.reset_index()
        for index, row in df.iterrows():
            print(index)
            check = False
            if row["direction"] == 1:
                for point in KulaiToLarkinData["route"]:
                    if(abs(point[0] - row["lat"]) < 3e-4 and abs(point[1] - row["long"]) < 3e-4):
                        check = True
                        break
            elif row["direction"] == 2:
                for point in LarkinToKulaiData["route"]:
                    if(abs(point[0] - row["lat"]) < 3e-4 and abs(point[1] - row["long"]) < 3e-4):
                        check = True
                        break
            if not check:
                df.drop(index, inplace=True)

        df.to_csv('./' + x + '_onRoute.csv', index=False)


def busStop():
    dataNames=['202203']
    colNames=['a','id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']
    for x in dataNames:
        df = pd.read_csv ('./' + x + '_onRoute.csv', names=colNames, skiprows=1)
        df = df.drop(['a'], axis=1)
        df = df.reset_index()
        last_direction = 0
        isBusStop = False
        for index, row in df.iterrows():
            isBusStop = False
            if row["direction"] == 1:
                for point in KulaiToLarkinData['stops']:
                    if(abs(point['loc'][0] - row["lat"]) < 3e-4 and abs(point['loc'][1] - row["long"]) < 3e-4):
                        if last_direction == 2 and point['code'] == 6001:
                            df.at[index, 'busStop'] = 7035
                            df.at[index, 'direction'] = 2
                            print("End of Route: " + str(index))
                        else:
                            df.at[index, 'busStop'] = point['code']
                        last_direction = 1
                        isBusStop = True
                        print(index)
                        break

            elif row["direction"] == 2:
                for point in LarkinToKulaiData['stops']:
                    if(abs(point['loc'][0] - row["lat"]) < 3e-4 and abs(point['loc'][1] - row["long"]) < 3e-4):
                        if last_direction == 1 and point['code'] == 7001:
                            df.at[index, 'busStop'] = 6031
                            df.at[index, 'direction'] = 1
                            print("End of Route: " + str(index))
                        else:
                            df.at[index, 'busStop'] = point['code']
                        last_direction = 2
                        isBusStop = True
                        print(index)
                        break
            if not isBusStop:
                df.at[index, 'busStop'] = 0
            

        #remove rows that are not bus stops or terminals
        # df = df.dropna(axis=0, subset=['busStop'])
        
        #remove redudant columns
        df = df.drop(['id', 'trip_id', 'bus_line_id','bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'bearing', 'status','created', 'updated' ], axis=1)

        #remove duplicate bus stops
        df = df[~((df['busStop'] == df['busStop'].shift(-1)) & (df['busStop'] != 0))]

        df.to_csv('./' + x + '_busStop.csv', index=False)


def cleanDirection():
    colNames=['index','socket_date','socket_datetime','lat','long','distance','speed','direction','busStop']

    dataNames=['202203']
    for x in dataNames:
        print(x)
        df = pd.read_csv ('./' + x + '_busStop.csv', names=colNames, skiprows=1)
        df = df.drop(['index'], axis=1)
        df['busStop'] = df['busStop'].astype(int)
        df['socket_date'] = pd.to_datetime(df['socket_date'])
        last_date = df.iloc[0]['socket_date']
        df = df.reset_index()
        indexToDrop = []
        lastBusStop = 0
        nextBusStop = 0
        #remove those that is not in full order
        for index, row in df.iterrows():
            print(index)
            if row['busStop'] ==  6001:
                check = True
                checkAll = True
                count = -1
                last_date = row['socket_date']
                nextBusStop = getNextBusStop(6001)
                busStopCount = 1
                while checkAll:
                    if (df.shift(count).loc[index]['busStop'] != 0):
                        if df.shift(count).loc[index]['busStop'] != nextBusStop or df.shift(count).loc[index]['socket_date'] != last_date:
                            check = False
                            checkAll = False
                        else:
                            busStopCount += 1
                            nextBusStop = getNextBusStop(nextBusStop)
                            if(math.floor(nextBusStop / 1000) != 6) or busStopCount == 31:
                                checkAll = False
                    count -= 1
                if not check:
                    indexToDrop.append({'depature':6001,'index': index})
                else:
                    lastBusStop = 6001
            elif row['busStop'] ==  7001:
                check = True
                checkAll = True
                count = -1
                last_date = row['socket_date']
                nextBusStop = getNextBusStop(7001)
                busStopCount = 1
                while checkAll:
                    if (df.shift(count).loc[index]['busStop'] != 0):
                        if df.shift(count).loc[index]['busStop'] != nextBusStop or df.shift(count).loc[index]['socket_date'] != last_date:
                            check = False
                            checkAll = False
                        else:
                            busStopCount += 1
                            nextBusStop = getNextBusStop(nextBusStop)
                            if(math.floor(nextBusStop / 1000) != 7) or busStopCount == 35:
                                checkAll = False
                    count -= 1
                if not check:
                    indexToDrop.append({'depature':7001,'index': index})
                else:
                    lastBusStop = 7001
            elif row['busStop'] != 0:
                if lastBusStop != row['busStop'] - 1:
                    indexToDrop.append({'depature':999,'index': index})
                else:
                    lastBusStop = row['busStop']
                if row['busStop'] == 6031 or row['busStop'] == 7035:
                    if df.shift(-1).loc[index]['busStop'] == 0:
                        indexToDrop.append({'depature': 999, 'index' : index + 1})
        
        df = df.reset_index()
        removeCount = 0
        endCount = 0
        for index, row in df.iterrows():
            print(index)
            if (row['busStop'] == 6001 or row['busStop'] == 7001) and index != indexToDrop[0]['index']:
                removeCount = 0
            if len(indexToDrop) == 0 and removeCount == 0:
                break
            if len(indexToDrop) > 0 and index == indexToDrop[0]['index']:
                #remove until next terminal or next index to drop
                endCount = 9999999999999999999999
                removeCount = 1
                indexToDrop.pop(0)

            if removeCount != 0:
                df.drop(index, inplace=True)
                if removeCount == endCount:
                    removeCount = 0
                else:
                    removeCount += 1
        print(indexToDrop)
        if df.iloc[-1]['busStop'] == 6001 or df.iloc[-1]['busStop'] == 7001:
            df = df[:-1]
        df.to_csv('./' + x + '_clean_direction.csv', index=False)

def getNextBusStop(currentBusStop):
    if math.floor(currentBusStop / 1000) == 6:
        if currentBusStop == 6031:
            return 7001
        else:
            return currentBusStop + 1
    
    if math.floor(currentBusStop / 1000) == 7:
        if currentBusStop == 7035:
            return 6001
        else:
            return currentBusStop + 1

def getTime():
    dataNames=['202203']
    colNames=['a','b','socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop']
    for x in dataNames:
        print(x)
        df = pd.read_csv ('./' + x + '_clean_direction.csv', names=colNames, skiprows=1)
        df = df.drop(['a','b'], axis=1)
        df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
        df = df.reset_index()
        last_dt = date.today()
        for index, row in df.iterrows():
            print(index)
            check = False
            if row["busStop"] == 6001 or row['busStop'] == 7001:
                last_dt =  row['socket_datetime']
                df.at[index, 'time_taken'] = 0
            elif row['busStop'] != 0:
                df.at[index, 'time_taken'] = int((pd.to_datetime(row['socket_datetime']) - last_dt).total_seconds())

        df['minuteOfDay'] = (df['socket_datetime'].dt.hour) * 60 + df['socket_datetime'].dt.minute
        df['day_of_week'] = df['socket_datetime'].dt.dayofweek

        df['lat'] = df['lat'].astype(float)
        df['long'] = df['long'].astype(float)
        df['direction'] = df['direction'].astype(int)
        df['busStop'] = df['busStop'].astype(int)
        df['day_of_week'] = df['day_of_week'].astype(int)
        df['minuteOfDay'] = df['minuteOfDay'].astype(int)

        df.to_csv('./' + x  + '_time.csv', index=False)


# onRoute()
# busStop()
# cleanDirection()
getTime()