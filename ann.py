import numpy as np
import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken', 'day_of_week','hour','minute','seconds']

df = pd.read_csv ('./dataset_timeOfDay/202203_timeOfDay.csv', names=colNames, skiprows=1)
df['time_taken'] = df['time_taken'].astype('int')
df['busStop'] = df['busStop'].astype('int')

df =  df[['busStop', 'day_of_week','hour','minute','seconds', 'time_taken']]
dataset = df.values

X = dataset[:,0:5]
Y = dataset[:,5]

from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
X_scale = min_max_scaler.fit_transform(X)

from sklearn.model_selection import train_test_split
X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X_scale, Y, test_size=0.3)
X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.5)


from keras.models import Sequential
from keras.layers import Dense
from keras import layers
from keras.optimizers import Adam

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

regressor = Sequential()

regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1))

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, Y_train, epochs = 100, batch_size = 32)
regressor.evaluate(X_test, Y_test)[1]
# model = Sequential([
#     layers.Input((5,1)),
#     layers.LSTM(64),
#     Dense(32, activation='relu'),
#     Dense(32, activation='relu'),
#     Dense(1, activation='sigmoid'),
# ])
# model.compile(optimizer=Adam(learning_rate = 0.001),
#               loss='mse',
#               metrics=['mean_absolute_error'])

# hist = model.fit(X_train, Y_train,
#           batch_size=32, epochs=100,
#           validation_data=(X_val, Y_val))

# model.evaluate(X_test, Y_test)[1]
print(X_train.shape, X_val.shape, X_test.shape, Y_train.shape, Y_val.shape, Y_test.shape)


# model = keras.Sequential()
# # Add an Embedding layer expecting input vocab of size 1000, and
# # output embedding dimension of size 64.
# model.add(layers.Embedding(input_dim=1000, output_dim=64))

# # Add a LSTM layer with 128 internal units.
# model.add(layers.LSTM(128))

# # Add a Dense layer with 10 units.
# model.add(layers.Dense(10))

# model.summary()