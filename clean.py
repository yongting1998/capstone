import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

dataNames=['202203']
for x in dataNames:
    print(x)
    colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

    df = pd.read_csv ('./dataset_onRoute/' + x + '_onRoute.csv', names=colNames, skiprows=1)

    df.drop(['id', 'trip_id', 'bus_line_id','bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'bearing', 'status','created', 'updated' ], axis=1, inplace=True)
    
    #remove previous row if value is same for direction at bus terminals
    #sometimes bus is at terminal for a long time
    df = df[~((df['direction'] == df['direction'].shift(-1)) & (df['direction'] > 2))]
    
    # df = df.reset_index()
    # lastTerminalIndex = 0
    # lastTerminal = 0
    # for indexCurrent, row in df.iterrows():
    #     if row["direction"] == 3:
    #         if lastTerminal == 3:
    #             df.drop(index=[lastTerminalIndex:indexCurrent], inplace=True)
    #         lastTerminal = 3
    #     if row["direction"] == 4:
    #         lastTerminal = 4


    df.to_csv('./dataset_clean/' + x + '_clean.csv', index=False)


# colNames=['a','b','id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

# df = pd.read_csv ('./dataset_onRoute/202203_onRoute.csv', names=colNames, skiprows=1)
# print(df['direction'].unique())
# # df.to_csv('./dataset_onRoute/202106_onRoute.csv')
