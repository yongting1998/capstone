import pandas as pd
import datetime
colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
for x in dataNames:
    print(x)
    df = pd.read_csv ('./dataset_onRoute/' + x + '_onRoute.csv', names=colNames, skiprows=1)

    # df.drop(['id', 'trip_id', 'bus_line_id','bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'bearing', 'status','created', 'updated' ], axis=1, inplace=True)

    df['socket_date'] = pd.to_datetime(df['socket_date'])
    df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
    df['day_of_week'] = df['socket_date'].dt.dayofweek
    df['hour'] = df['socket_datetime'].dt.hour
    df['minute'] = df['socket_datetime'].dt.minute
    df['second'] = df['socket_datetime'].dt.second

    df.to_csv('./dataset_day/' + x  + '_day.csv', index=False)