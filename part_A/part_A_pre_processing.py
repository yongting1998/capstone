import pandas as pd
from datetime import date
import datetime as dt
import matplotlib.pyplot as plt
import json
import numpy as np

fKulaiToLarkin = open('../dataset/KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('../dataset/LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

def timeTaken():
    colNames=['a','index','socket_date','socket_datetime','lat','long','distance','speed','direction','busStop']

    dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/dataset_clean_direction/' + x + '_clean_direction.csv', names=colNames, skiprows=1)

        df = df.drop(['a','index'], axis=1)
        df = df.reset_index()
        last_dt = date.today()
        for index, row in df.iterrows():
            print(index)
            check = False
            if row["busStop"] == 6001 or row['busStop'] == 7001:
                last_dt =  pd.to_datetime(row['socket_datetime'])
                df.at[index, 'time_taken'] = 0
            else:
                df.at[index, 'time_taken'] = int((pd.to_datetime(row['socket_datetime']) - last_dt).total_seconds())

        df.to_csv('../dataset/part_A/dataset_timeTaken/' + x  + '_timeTaken.csv', index=False)


def timeOfDay():
    dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
    colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken']
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/part_A/dataset_timeTaken/' + x + '_timeTaken.csv', names=colNames, skiprows=1)

        df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
        df['day_of_week'] = df['socket_datetime'].dt.dayofweek
        df['hour'] = df['socket_datetime'].dt.hour
        df['minute'] = df['socket_datetime'].dt.minute
        df['seconds'] = df['socket_datetime'].dt.second

        df.to_csv('../dataset/part_A/dataset_timeOfDay/' + x  + '_timeOfDay.csv', index=False)

def minute():
    dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
    colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken','day_of_week','hour','minute','seconds']
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/part_A/dataset_timeOfDay/' + x + '_timeOfDay.csv', names=colNames, skiprows=1)
        df = df.drop(['hour', 'minute', 'seconds'], axis=1)
        df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
        df['minuteOfDay'] = (df['socket_datetime'].dt.hour) * 60 + df['socket_datetime'].dt.minute

        df['lat'] = df['lat'].astype(float)
        df['long'] = df['long'].astype(float)
        df['direction'] = df['direction'].astype(int)
        df['busStop'] = df['busStop'].astype(int)
        df['time_taken'] = df['time_taken'].astype(int)
        df['day_of_week'] = df['day_of_week'].astype(int)
        df['minuteOfDay'] = df['minuteOfDay'].astype(int)

        df.to_csv('../dataset/part_A/dataset_minute/' + x  + '_minute.csv', index=False)

        #remember to manually remove header from dataset as its appending
        if x != '202203':
            df.to_csv('../dataset/part_A/dataset_minute/full_minute.csv', index=False, mode='a')


def outlier():
    colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken', 'day_of_week', 'minuteOfDay']
    df = pd.read_csv ('../dataset/part_A/dataset_minute/full_minute.csv', names=colNames, skiprows=1)
    listOfBusStops=[]    
    cols = ['time_taken']
    figure, axis = plt.subplots(2,2)
    figure.suptitle('before cleaning')
    countX = 0
    countY = 0
    for i in range(1,32):
        listOfBusStops.append(6000 + i)
    for i in range(36):
        listOfBusStops.append(7000 + i)
    df['time_taken'] = df['time_taken'].astype(int)
    print(df[df['time_taken'] > 10000])
    # df = df.loc[df['time_taken'] < 10000]
    df_clean = pd.DataFrame()
    for busStop in listOfBusStops:
        dfTemp = df.loc[df['busStop'] == busStop]
        originalSize = int(dfTemp.size)
        if(busStop > 6001 and busStop < 6006):
            axis[countX, countY].plot(dfTemp['socket_date'],dfTemp['time_taken'])
            axis[countX, countY].set_title(busStop)
            if(countY == 1):
                countX += 1
                countY = 0
            else:
                countY += 1
        Q1 = dfTemp[cols].quantile(0.05)
        Q3 = dfTemp[cols].quantile(0.95)
        IQR = Q3 - Q1
        if(busStop != 6001 and busStop != 7001):
            dfTemp = dfTemp[~((dfTemp[cols] < (Q1 - 1.5 * IQR)) |(dfTemp[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
        df_clean = pd.concat([df_clean, dfTemp], sort=False)
            # print("reduced:  "  + str(originalSize - int(dfTemp.size)))


    df_clean.to_csv('../dataset/part_A/dataset_outlier/full_outlier.csv', index=False)
    # df.to_csv('../dataset/part_A/dataset_outlier/full_outlier.csv', index=False, mode='a')


    plt.show()
    figure, axis = plt.subplots(2,2)
    figure.suptitle('after cleaning')
    countX = 0
    countY = 0
    for busStop in listOfBusStops:
        dfTemp = df.loc[df['busStop'] == busStop]
        if(busStop > 6001 and busStop < 6006):
            axis[countX, countY].plot(dfTemp['socket_date'],dfTemp['time_taken'])
            axis[countX, countY].set_title(busStop)
            if(countY == 1):
                countX += 1
                countY = 0
            else:
                countY += 1

    plt.show()

def distance():
    dataNames=['202105','202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201', '202202', '202203']
    colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken','day_of_week','minuteOfDay']
    for x in dataNames:
        df = pd.read_csv ('../dataset/part_A/dataset_minute/' + x + '_minute.csv', names=colNames, skiprows=1)
        df = df.reset_index()
        for index, row in df.iterrows():
            print(index)
            if row["direction"] == 1:
                for point in KulaiToLarkinData['stops']:
                    if row['busStop'] == point['code']:
                        df.at[index, 'distanceToNext'] = point['distanceToNext']
                        break
            elif row["direction"] == 2:
                for point in LarkinToKulaiData['stops']:
                    if row['busStop'] == point['code']:
                        df.at[index, 'distanceToNext'] = point['distanceToNext']
                        break

        df.to_csv('../dataset/part_A/dataset_distance/' + x + '_distance.csv', index=False)


# timeTaken()
# timeOfDay()
# minute()
outlier()

# distance()
