import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plotData():
    colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken', 'day_of_week', 'minuteOfDay']
    df = pd.read_csv ('../dataset/part_A/dataset_outlier/full_outlier.csv', names=colNames, skiprows=1)
    KulaiToLarkinBusStops=[]   
    LarkinToKulaiBusStops=[]    
    cols = ['time_taken']
    KulaiToLarkinFigure, KulaiToLarkinAxis = plt.subplots(6,6)
    KulaiToLarkinFigure.suptitle('Kulai To Larkin')
    LarkinToKulaiFigure, LarkinToKulaiAxis = plt.subplots(6,6)
    LarkinToKulaiFigure.suptitle('Larkin To Kulai')
    countX = 0
    countY = 0
    for i in range(1,32):
        KulaiToLarkinBusStops.append(6000 + i)
    for i in range(36):
        LarkinToKulaiBusStops.append(7000 + i)
    df['time_taken'] = df['time_taken'].astype(int)
    for busStop in KulaiToLarkinBusStops:
        dfTemp = df.loc[df['busStop'] == busStop]
        KulaiToLarkinAxis[countX, countY].plot(dfTemp['socket_date'],dfTemp['time_taken'])
        KulaiToLarkinAxis[countX, countY].set_title(busStop)
        if(countY == 5):
            countX += 1
            countY = 0
        else:
            countY += 1
    countX = 0
    countY = 0
    for busStop in LarkinToKulaiBusStops:
        dfTemp = df.loc[df['busStop'] == busStop]
        LarkinToKulaiAxis[countX, countY].plot(dfTemp['socket_date'],dfTemp['time_taken'])
        LarkinToKulaiAxis[countX, countY].set_title(busStop)
        if(countY == 5):
            countX += 1
            countY = 0
        else:
            countY += 1
    
    KulaiToLarkinFigure.show()
    LarkinToKulaiFigure.show()
    input()

plotData()