
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

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
    
    
    axis[countX, countY].plot(df['time_taken'])
    print(countX,countY)
    if countY == 2:
        countX += 1
        countY = 0
    else:
        countY += 1

    df = df[(df.time_taken < 10000) & (df.time_taken > 0)]
    
    df.to_csv('../dataset/part_A/dataset_outlier/' + x + '_outlier.csv', index=False)
    df.to_csv('../dataset/part_A/dataset_outlier/full_outlier.csv', index=False, mode='a')

    # cols = ['time_taken']

    # Q1 = df[cols].quantile(0.05)
    # Q3 = df[cols].quantile(0.95)
    # IQR = Q3 - Q1
    # df = df[~((df[cols] < (Q1 - 1.5 * IQR)) |(df[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

plt.show()

figure, axis = plt.subplots(4, 3)
figure.suptitle('before cleaning')
countX = 0
countY = 0
colNames.remove('index')
for x in dataNames:
    print(x)
    df = pd.read_csv ('../dataset/part_A/dataset_outlier/'+ x + '_outlier.csv', names=colNames, skiprows=1)
    axis[countX, countY].plot(df['time_taken'])
    print(countX,countY)
    if countY == 2:
        countX += 1
        countY = 0
    else:
        countY += 1

plt.show()

