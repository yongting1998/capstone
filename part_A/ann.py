import numpy as np
import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# importing the libraries
from keras.models import Sequential
from keras.layers import Dense
from sklearn import metrics
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

def ann(X_test, y_test, X_train, y_train, batch_size, epoch, input_dim):
        # create ANN model
    model = Sequential()
    
    # Defining the Input layer and FIRST hidden layer, both are same!
    model.add(Dense(units=50, input_dim=input_dim, kernel_initializer='normal', activation='relu'))
    
    # Defining the Second layer of the model
    # after the first layer we don't have to specify input_dim as keras configure it automatically
    model.add(Dense(units=50, kernel_initializer='normal', activation='tanh'))
    
    # The output neuron is a single fully connected node 
    # Since we will be predicting a single number
    model.add(Dense(1, kernel_initializer='normal'))
    
    # Compiling the model
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    # Fitting the ANN to the Training set
    model.fit(X_train, y_train ,batch_size = batch_size, epochs = epoch, verbose=1)
    MAPE = np.mean(100 * (np.abs(model.predict(X_test))/y_test))
    print(MAPE)
    
    
    y_pred = model.predict(X_test)
    return y_pred

def trainParameters(X_test, y_test, X_train, y_train, input_dim):
    batch_size_list = [10,20,30,40,50,60,70,80,90,100,150,200,250,300]
    epoch_list = [10,20,30,40,50,60,70,80,90,100,150,200,250,300]
    results = []

    for batch_size in batch_size_list:
        for epoch in epoch_list:
            y_pred = ann(X_test, y_test, X_train, y_train, batch_size, epoch, input_dim)
            MAPE = np.mean(100 * (np.abs(y_pred)/y_test))
            results.append("batch: " + str(batch_size) + " - epoch:" + str(epoch) + " - accuracy:" + str(100-MAPE))

    for result in results:
        print(result)

def trainData(X_test, y_test, X_train, y_train, input_dim):
    y_pred = ann(X_test, y_test, X_train, y_train,200,500, input_dim)

    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    plt.plot(y_test)
    plt.plot(y_pred)
    plt.show()

def scale(data, input_dim):
    TargetVariable=['time_taken']
    Features = []
    if input_dim == 3:
        Features=['busStop', 'day_of_week','minuteOfDay']
    elif input_dim == 4:
        Features=['busStop', 'day_of_week','minuteOfDay', 'distanceToNext']



    X = data[Features].values
    y = data[TargetVariable].values
    print(X.shape)
    print(y.shape)


    scalerX = preprocessing.StandardScaler()
    scalerY = preprocessing.StandardScaler()
    X_scale = scalerX.fit(X)
    y_scale = scalerY.fit(y)

    X = X_scale.transform(X)
    y = y_scale.transform(y)

    return X, y
    


colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken', 'day_of_week', 'minuteOfDay']
df = pd.read_csv ('../dataset/part_A/dataset_minute/202203_minute.csv', names=colNames, skiprows=1)
input_dim = 3

# colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken', 'day_of_week', 'minuteOfDay', 'distanceToNext']
# df = pd.read_csv ('../dataset/part_A/dataset_distance/202203_distance.csv', names=colNames, skiprows=1)
# input_dim = 4

df['time_taken'] = df['time_taken'].astype('int')
df['busStop'] = df['busStop'].astype('int')

X, y = scale(df[['busStop', 'day_of_week','minuteOfDay', 'time_taken']], input_dim)

# X, y = scale(df[['busStop', 'day_of_week','minuteOfDay', 'distanceToNext', 'time_taken']], input_dim)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

trainData(X_test, y_test, X_train, y_train, input_dim)
#trainParameters(X_test, y_test, X_train, y_train, input_dim)

