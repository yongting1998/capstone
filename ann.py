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

def trainData(X_test, y_test, X_train, y_train):
        # create ANN model
    model = Sequential()
    
    # Defining the Input layer and FIRST hidden layer, both are same!
    model.add(Dense(units=50, input_dim=3, kernel_initializer='normal', activation='relu'))
    
    # Defining the Second layer of the model
    # after the first layer we don't have to specify input_dim as keras configure it automatically
    model.add(Dense(units=50, kernel_initializer='normal', activation='tanh'))
    
    # The output neuron is a single fully connected node 
    # Since we will be predicting a single number
    model.add(Dense(1, kernel_initializer='normal'))
    
    # Compiling the model
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    # Fitting the ANN to the Training set
    model.fit(X_train, y_train ,batch_size = 200, epochs = 500, verbose=1)
    MAPE = np.mean(100 * (np.abs(y_test-model.predict(X_test))/y_test))
    print(MAPE)
    
    
    y_pred = model.predict(X_test)
    print(y_pred)
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    plt.plot(y_test)
    plt.plot(y_pred)
    plt.show()
    


colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken', 'day_of_week', 'minuteOfDay']

df = pd.read_csv ('./dataset_minute/202203_minute.csv', names=colNames, skiprows=1)
df['time_taken'] = df['time_taken'].astype('int')
df['busStop'] = df['busStop'].astype('int')

# df =  df[['busStop', 'day_of_week','minuteOfDay', 'time_taken']]
TargetVariable=['time_taken']
Predictors=['busStop', 'day_of_week','minuteOfDay']


from sklearn.preprocessing import StandardScaler
# df[['minuteOfDay']] = sc.fit_transform(df[['minuteOfDay']])

X = df[Predictors].values
y = df[TargetVariable].values
print(X.shape)
print(y.shape)

from sklearn import preprocessing
scalerX = preprocessing.StandardScaler()
scalerY = preprocessing.StandardScaler()
X_scale = scalerX.fit(X)
y_scale = scalerY.fit(y)

X = X_scale.transform(X)
y = y_scale.transform(y)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

trainData(X_test, y_test, X_train, y_train)



# from sklearn.metrics import mean_squared_error as MSE
# from sklearn import neural_network
# from sklearn.metrics import r2_score
# from sklearn import metrics

# print("Activation Function: identity")

# model = neural_network.MLPRegressor(hidden_layer_sizes=(150,100,50),
#                        max_iter = 300,activation = 'relu',
#                        solver = 'adam')
# model.fit(X_train, Y_train)
# y_pred = model.predict(X_test)






# from keras.models import Sequential
# from keras.layers import Dense
# from keras import layers
# from keras.optimizers import Adam

# from keras.layers import LSTM
# from keras.layers import Dropout

# regressor = Sequential()

# regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
# regressor.add(Dropout(0.2))

# regressor.add(LSTM(units = 50, return_sequences = True))
# regressor.add(Dropout(0.2))

# regressor.add(LSTM(units = 50, return_sequences = True))
# regressor.add(Dropout(0.2))

# regressor.add(LSTM(units = 50))
# regressor.add(Dropout(0.2))

# regressor.add(Dense(units = 1))

# regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# regressor.fit(X_train, Y_train, epochs = 500, batch_size = 32)
# print(regressor.evaluate(X_test, y_test)[1])


# model = Sequential([
#     layers.Input((3,1)),
#     layers.LSTM(64),
#     Dense(32, activation='relu'),
#     Dense(32, activation='relu'),
#     Dense(1, activation='sigmoid'),
# ])
# model.compile(optimizer='sgd',
#               loss='binary_crossentropy',
#               metrics=['accuracy'])

# hist = model.fit(X_train, Y_train,
#           batch_size=32, epochs=100,
#           validation_data=(X_val, Y_val))

# model.evaluate(X_test, y_test)[1]
# print(X_train.shape, X_val.shape, X_test.shape, Y_train.shape, Y_val.shape, y_test.shape)


# model = keras.Sequential()
# # Add an Embedding layer expecting input vocab of size 1000, and
# # output embedding dimension of size 64.
# model.add(layers.Embedding(input_dim=1000, output_dim=64))

# # Add a LSTM layer with 128 internal units.
# model.add(layers.LSTM(128))

# # Add a Dense layer with 10 units.
# model.add(layers.Dense(10))

# model.summary()