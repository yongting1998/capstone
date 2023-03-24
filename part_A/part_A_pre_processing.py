import pandas as pd
from datetime import date
import datetime as dt
import matplotlib.pyplot as plt
import json

fKulaiToLarkin = open('../dataset/KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('../dataset/LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

def timeTaken():
    colNames=['index','socket_date','socket_datetime','lat','long','distance','speed','direction','busStop']

    dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/dataset_busStop/' + x + '_busStop.csv', names=colNames, skiprows=1)

        df = df.drop(['index'], axis=1)
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



def outlier():
    colNames=['index', 'socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken']
    dataNames=['202105','202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201', '202202', '202203']

    figure, axis = plt.subplots(4, 3)
    figure.suptitle('before cleaning')
    countX = 0
    countY = 0
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/part_A/dataset_timeTaken/'+ x + '_timeTaken.csv', names=colNames, skiprows=1)

        df = df.drop(['index'], axis=1)
        
        
        axis[countX, countY].plot(df['time_taken'],df['socket_date'])
        print(countX,countY)
        if countY == 2:
            countX += 1
            countY = 0
        else:
            countY += 1

        #df = df[(df.time_taken < 10000) & (df.time_taken >= 0)]
        
        cols = ['time_taken']

        Q1 = df[cols].quantile(0.05)
        Q3 = df[cols].quantile(0.95)
        IQR = Q3 - Q1
        df = df[~((df[cols] < (Q1 - 1.5 * IQR)) |(df[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]


        
        df.to_csv('../dataset/part_A/dataset_outlier/' + x + '_outlier.csv', index=False)
        df.to_csv('../dataset/part_A/dataset_outlier/full_outlier.csv', index=False, mode='a')


    plt.show()

    figure, axis = plt.subplots(4, 3)
    figure.suptitle('before cleaning')
    countX = 0
    countY = 0
    colNames.remove('index')
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/part_A/dataset_outlier/'+ x + '_outlier.csv', names=colNames, skiprows=1)
        axis[countX, countY].plot(df['time_taken'], df['socket_date'])
        print(countX,countY)
        if countY == 2:
            countX += 1
            countY = 0
        else:
            countY += 1

    plt.show()

def timeOfDay():
    dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
    colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken']
    for x in dataNames:
        print(x)
        df = pd.read_csv ('../dataset/part_A/dataset_outlier/' + x + '_outlier.csv', names=colNames, skiprows=1)

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

        df.to_csv('../dataset/part_A/dataset_minute/' + x  + '_minute.csv', index=False)
        df.to_csv('../dataset/part_A/dataset_minute/full_minute.csv', index=False, mode='a')

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


timeTaken()
outlier()
timeOfDay()
minute()
# distance()
