

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn import metrics
from sklearn import preprocessing
import joblib

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import random

def load_data():
    colNames=['index','socket_date','socket_datetime','lat','long','distance','speed','direction','busStop','time_taken','minuteOfDay','day_of_week']
    df = pd.read_csv ('./202203_time.csv', names=colNames, skiprows=1)
    df = df.drop(['index'], axis=1)
    df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
    dfPositions = pd.DataFrame(columns=colNames[1:])
    dfLength = df.shape[0]
    randomIndex = random.sample(range(5, dfLength), 50)
    count = 0
    for index in randomIndex:
        if not df.iloc[index]['busStop']:
            for i in range(1,dfLength):
                if df.shift(-i).iloc[index]['busStop']:
                    dfPositions.loc[count] = df.iloc[index]
                    dfPositions.loc[count + 1] = df.shift(-i).iloc[index]
                    dfPositions.at[count, 'time_taken_to_stop'] = int((pd.to_datetime(df.shift(-i).iloc[index]['socket_datetime']) - pd.to_datetime(df.iloc[index]['socket_datetime'])).total_seconds())
                    count += 2
                    break

    scalerX = joblib.load('../scalerX.save') 
    scalerY = joblib.load('../scalerY.save')
    print(dfPositions)
    
    model = keras.models.load_model("../model.h5")
    actualTime = []
    predictedTime = []
    yPredList = []
    yActualList = []
    for i in range(0,dfPositions.shape[0],2):
        loc_time_taken_to_next_stop = dfPositions.iloc[i]['time_taken_to_stop']
        loc_time_taken = dfPositions.iloc[i]['time_taken']
        minuteOfDay = dfPositions.iloc[i]['minuteOfDay']
        day_of_week = dfPositions.iloc[i]['day_of_week']
        target_busStop = dfPositions.iloc[i+1]['busStop']
        X = scalerX.transform([[target_busStop, day_of_week, minuteOfDay]])
        y_pred = model.predict(X)
        y_pred_scale_inverse = scalerY.inverse_transform(y_pred)
        predicted_time_to_next_stop = y_pred_scale_inverse[0][0] - loc_time_taken

        yPredList.append(y_pred_scale_inverse[0][0])
        yActualList.append(dfPositions.iloc[i+1]['time_taken'])
        actualTime.append(loc_time_taken_to_next_stop)
        predictedTime.append(predicted_time_to_next_stop)

    print(predictedTime)
    xAxis = []
    for i in range(len(actualTime)):
        xAxis.append(i)

    plt.plot(xAxis, yPredList, label="Predicted")
    plt.plot(xAxis, yActualList, label="Actual")
    plt.legend()
    plt.show()


    plt.plot(xAxis, predictedTime, label="Predicted")
    plt.plot(xAxis, actualTime, label="Actual")
    plt.legend()
    plt.show()
    # Features=['busStop', 'day_of_week','minuteOfDay']
    # TargetVariable=['time_taken']
    # X = scalerX.transform(df[Features].values)
    # y = df[TargetVariable].values
    # return X,y

def test():
    model = keras.models.load_model("../model.h5")
    scalerY = joblib.load('../scalerY.save')
    print(model.summary())
    X,y = load_data()
    y_pred = model.predict(X)
    y_pred_scale_inverse = scalerY.inverse_transform(y_pred)
    APE=100*(abs(y-y_pred_scale_inverse)/y_pred_scale_inverse)
    print('The Accuracy of ANN model is:', 100-np.mean(APE))
    print(y)
    # plt.plot(y_pred_scale_inverse, label = "Predicted")
    plt.plot(y, label = "Actual")
    plt.legend()
    plt.show()

# test()
load_data()
