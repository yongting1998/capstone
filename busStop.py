import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

dataNames=['202105','202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201', '202202', '202203']
colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']
for x in dataNames:
    df = pd.read_csv ('./dataset_onRoute/' + x + '_onRoute.csv', names=colNames, skiprows=1)
    # df = df [600000:]
    df = df.reset_index()
    for index, row in df.iterrows():
        print(index)
        if row["direction"] == 1:
            for point in KulaiToLarkinData['stops']:
                if(abs(point['loc'][0] - row["lat"]) < 1e-4 and abs(point['loc'][1] - row["long"]) < 1e-4):
                    df.at[index, 'busStop'] = point['code']
                    break
        elif row["direction"] == 2:
            for point in LarkinToKulaiData['stops']:
                if(abs(point['loc'][0] - row["lat"]) < 1e-4 and abs(point['loc'][1] - row["long"]) < 1e-4):
                    df.at[index, 'busStop'] = point['code']
                    break
        elif row["direction"] == 3:
            df.at[index, 'busStop'] = 3
        elif row["direction"] == 4:
            df.at[index, 'busStop'] = 4

    #remove rows that are not bus stops or terminals
    df = df.dropna(axis=0, subset=['busStop'])
    
    #remove duplicate bus stops
    df = df[~(df['busStop'] == df['busStop'].shift(-1))]

    #remove redudant columns
    df = df.drop(['id', 'trip_id', 'bus_line_id','bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'bearing', 'status','created', 'updated' ], axis=1)

    df.to_csv('./dataset_busStop/' + x + '_busStop.csv', index=False)