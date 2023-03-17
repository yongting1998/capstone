import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np

def getDirection():
   
    dataNames=['202105','202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201', '202202', '202203']
    colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated']
    for x in dataNames:
        df = pd.read_csv ('../dataset/dataset_original/' + x + '.csv', names=colNames, skiprows=1)
        if( x != '202112'):
            df["lat"] = df["lat"].str[1:].astype(float)
            df["long"] = df["long"].str[:-1].astype(float)

        last_station = ""
        df = df.reset_index()
        for index, row in df.iterrows():
            print(index)
            # kulai station
            if(abs(1.66246 - row["lat"]) < 3e-4 and abs(103.59879 - row["long"]) < 3e-4):
                last_station = "kulai"
                df.at[index, 'direction'] = 1
            # larkin station
            elif(abs(1.495100 - row["lat"]) < 3e-4 and abs(103.741749 - row["long"]) < 3e-4):
                last_station = "larkin"
                df.at[index, 'direction'] = 2
            else:
                #kulai to larkin -> 1
                #larkin to kulai -> 2
                if last_station == "kulai":
                    print("YES KULAI")
                    df.at[index, 'direction'] = 1
                elif last_station == "larkin":
                    df.at[index, 'direction'] = 2
                else:
                    df.at[index, 'direction'] = 0

        df["direction"] = df["direction"].astype(int)
        df.to_csv('../dataset/dataset_direction/' + x + '_direction.csv')


def getBusStops():
    fKulaiToLarkin = open('../dataset/KulaiToLarkin.json')
    KulaiToLarkinData = json.load(fKulaiToLarkin)
    fLarkinToKulai = open('../dataset/LarkinToKulai.json')
    LarkinToKulaiData = json.load(fLarkinToKulai)

   
    dataNames=['202105','202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201', '202202', '202203']
    colNames=['a','b', 'id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']
    for x in dataNames:
        df = pd.read_csv ('../dataset/dataset_direction/' + x + '_direction.csv', names=colNames, skiprows=1)
        df = df.drop(['a', 'b'], axis=1)
        df = df.reset_index()
        last_direction = 0
        for index, row in df.iterrows():
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
                        break

        #remove rows that are not bus stops or terminals
        df = df.dropna(axis=0, subset=['busStop'])
        
        #remove redudant columns
        df = df.drop(['id', 'trip_id', 'bus_line_id','bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'bearing', 'status','created', 'updated' ], axis=1)

        #remove duplicate bus stops
        df = df[~(df['busStop'] == df['busStop'].shift(-1))]

        df.to_csv('../dataset/dataset_busStop/' + x + '_busStop.csv', index=False)


#getDirection()
getBusStops()

