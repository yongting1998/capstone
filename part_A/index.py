import pandas as pd
import numpy as np

colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken', 'day_of_week', 'minuteOfDay']
df = pd.read_csv ('../dataset/part_A/dataset_minute/full_minute.csv', names=colNames, skiprows=1)

df['time_taken'] = df['time_taken'].astype('int')
df['busStop'] = df['busStop'].astype('int')
print(df.dtypes)