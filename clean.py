import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
for x in dataNames:
    print(x)
    colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

    df = pd.read_csv ('./dataset_onRoute/' + x + '_onRoute.csv', names=colNames, skiprows=1)

    df.drop(['id', 'trip_id', 'bus_line_id','bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'bearing', 'status','created', 'updated' ], axis=1, inplace=True)

    df.to_csv('./dataset_clean/' + x + '_clean.csv', index=False)


# colNames=['a','b','id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

# df = pd.read_csv ('./dataset_onRoute/202203_onRoute.csv', names=colNames, skiprows=1)
# print(df['direction'].unique())
# # df.to_csv('./dataset_onRoute/202106_onRoute.csv')
