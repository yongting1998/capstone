import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

df = pd.read_csv ('./dataset_direction/202105_direction.csv', names=colNames, skiprows=1)

df = df.reset_index()
for index, row in df.iterrows():
    print(index)
    if row["direction"] == 1:
        for point in KulaiToLarkinData:
            if(abs(point[0] - row["lat"]) < 1e-4 and abs(point[1] - row["long"]) < 1e-4):
                df.drop(index, inplace=True)
                break
    elif row["direction"] == 2:
        for point in LarkinToKulaiData:
            if(abs(point[0] - row["lat"]) < 1e-4 and abs(point[1] - row["long"]) < 1e-4):
                df.drop(index, inplace=True)
                break

df.to_csv('./dataset_onRoute/202105_onRoute.csv')

plt.scatter(x=df['lat'], y=df['long'])
plt.show()