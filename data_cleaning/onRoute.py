import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

dataNames=['202105']
colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

for x in dataNames:
    df = pd.read_csv ('./dataset_direction/' + x + '_direction.csv', names=colNames, skiprows=1)
    #df = df [600000:]
    df = df.reset_index()
    for index, row in df.iterrows():
        print(index)
        check = False
        if row["direction"] == 1:
            for point in KulaiToLarkinData:
                if(abs(point[0] - row["lat"]) < 2e-4 and abs(point[1] - row["long"]) < 2e-4):
                    check = True
                    break
        elif row["direction"] == 2:
            for point in LarkinToKulaiData:
                if(abs(point[0] - row["lat"]) < 2e-4 and abs(point[1] - row["long"]) < 2e-4):
                    check = True
                    break
        elif row["direction"] == 3 or row["direction"] == 4:
            check = True
        if not check:
            df.drop(index, inplace=True)

    df.to_csv('./dataset_onRoute/' + x + '_onRoute.csv', mode='a')
