import pandas as pd
import datetime as dt

dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken']
for x in dataNames:
    print(x)
    df = pd.read_csv ('../dataset_outlier/' + x + '_outlier.csv', names=colNames, skiprows=1)

    df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
    df['day_of_week'] = df['socket_datetime'].dt.dayofweek
    df['hour'] = df['socket_datetime'].dt.hour
    df['minute'] = df['socket_datetime'].dt.minute
    df['seconds'] = df['socket_datetime'].dt.second

    df.to_csv('../dataset_timeOfDay/' + x  + '_timeOfDay.csv', index=False)
