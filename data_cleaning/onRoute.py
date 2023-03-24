import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


fKulaiToLarkin = open('../dataset/KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('../dataset/LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

dataNames=['202203']
colNames=['a','b','id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

for x in dataNames:
    df = pd.read_csv ('../dataset/dataset_direction/' + x + '_direction.csv', names=colNames, skiprows=1)
    df = df.drop(['a', 'b'], axis=1)
    df['lat'] = df['lat'].astype(float)
    df['long'] = df['long'].astype(float)
    #df = df [600000:]
    df = df.reset_index()
    for index, row in df.iterrows():
        print(index)
        check = False
        if row["direction"] == 1:
            for point in KulaiToLarkinData["stops"]:
                if(abs(point['loc'][0] - row["lat"]) < 3e-4 and abs(point['loc'][1] - row["long"]) < 3e-4):
                    check = True
                    break
        elif row["direction"] == 2:
            for point in LarkinToKulaiData["stops"]:
                if(abs(point['loc'][0] - row["lat"]) < 3e-4 and abs(point['loc'][1] - row["long"]) < 3e-4):
                    check = True
                    break

        if not check:
            df.drop(index, inplace=True)

    df.to_csv('../testing/' + x + '_onRoute.csv', mode='a')
