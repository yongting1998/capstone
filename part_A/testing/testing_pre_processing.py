import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


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

# onRoute()
busStop()