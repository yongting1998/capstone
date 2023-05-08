import pandas as pd
from datetime import date
import datetime as dt
import os
import matplotlib.pyplot as plt
import json
import numpy as np

def time_taken():
    colNames=['index','socket_date','socket_datetime','lat','long','distance','speed','direction','busStop']
    dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/dataset_clean_direction/' + x + '_clean_direction.csv', names=colNames, skiprows=1)

        df = df.drop(['index'], axis=1)
        df = df.reset_index()
        last_dt = date.today()
        # for i in range(6001,6032):
        #     df[i] = 0
        # for i in range(7001,7036):
        #     df[i] = 0
        for index, row in df.iterrows():
            if(row['busStop'] != 6001 and row['busStop'] != 7001):
                df.at[index, 'time_taken'] = int((pd.to_datetime(row['socket_datetime']) - last_dt).total_seconds())
            else:
                df.at[index, 'time_taken'] = 0
            last_dt = pd.to_datetime(row['socket_datetime'])

        for i in range(6001, 6032):
            dfTemp = df[df['busStop'] == i]
            if not os.path.isfile('../dataset/part_B/dataset_timeTaken/' + str(i)  + '_timeTaken.csv'):
                dfTemp.to_csv('../dataset/part_B/dataset_timeTaken/' + str(i)  + '_timeTaken.csv', index=False,)
            else:
                dfTemp.to_csv('../dataset/part_B/dataset_timeTaken/' + str(i)  + '_timeTaken.csv', index=False, header=False, mode='a')
        for i in range(7001, 7036):
            dfTemp = df[df['busStop'] == i]
            if not os.path.isfile('../dataset/part_B/dataset_timeTaken/' + str(i)  + '_timeTaken.csv'):
                dfTemp.to_csv('../dataset/part_B/dataset_timeTaken/' + str(i)  + '_timeTaken.csv', index=False,)
            else:
                dfTemp.to_csv('../dataset/part_B/dataset_timeTaken/' + str(i)  + '_timeTaken.csv', index=False, header=False, mode='a')

def timeOfDay():
    colNames=['index','socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken']
    dataNames = []
    for i in range(6001, 6032):
        dataNames.append(str(i))
    for i in range(7001, 7036):
        dataNames.append(str(i))
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/part_B/dataset_timeTaken/' + x + '_timeTaken.csv', names=colNames, skiprows=1)
        df = df.drop(['index'], axis=1)

        df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
        df['day_of_week'] = df['socket_datetime'].dt.dayofweek
        df['minuteOfDay'] = (df['socket_datetime'].dt.hour) * 60 + df['socket_datetime'].dt.minute

        df.to_csv('../dataset/part_B/dataset_timeOfDay/' + x  + '_timeOfDay.csv', index=False)

def plot():
    colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken','day_of_week','minuteOfDay']
    dataNames = []
    for i in range(6001, 6032):
        dataNames.append(str(i))
    for i in range(7001, 7036):
        dataNames.append(str(i))

    cols = ['time_taken']
    figure, axis = plt.subplots(2,2)
    figure.suptitle('before cleaning')
    countX = 0
    countY = 0
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/part_B/dataset_timeOfDay/' + x + '_timeOfDay.csv', names=colNames, skiprows=1)
        df['time_taken'] = df['time_taken'].astype(int)
        if(int(x) > 6001 and int(x) < 6006):
            axis[countX, countY].plot(df['socket_date'],df['time_taken'])
            axis[countX, countY].set_title(x)
            if(countY == 1):
                countX += 1
                countY = 0
            else:
                countY += 1
    plt.show()

def average_travelling_time():
    colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken','day_of_week','minuteOfDay']
    dataNames = []
    list_of_hour = {}
    for i in range(6001, 6032):
        dataNames.append(str(i))
    for i in range(7001, 7036):
        dataNames.append(str(i))
    for i in range(24):
        list_of_hour[str(i)] = []
    
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/part_B/dataset_timeOfDay/' + x + '_timeOfDay.csv', names=colNames, skiprows=1)
        df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
        df['hour'] = df['socket_datetime'].dt.hour
        df = df.loc[df['time_taken'] > 0]
        for i in range(24):
            list_of_hour[str(i)] += df.loc[df['hour'] == i, 'time_taken'].tolist()
    
    for i in range(24):
        size = len(list_of_hour[str(i)])
        if(size > 0):
            average_time = sum(list_of_hour[str(i)])/size
            print("HOUR " + str(i) +":  " + str(average_time))
        else:
            print("HOUR " + str(i) +":  0")

    


# time_taken()
# timeOfDay()
# outlier()
average_travelling_time()