import pandas as pd
from datetime import date
colNames=['index','socket_date','socket_datetime','lat','long','distance','speed','direction','busStop']

dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
for x in dataNames:
    print(x)
    df = pd.read_csv ('../dataset/dataset_busStop/' + x + '_busStop.csv', names=colNames, skiprows=1)

    # df.drop(['id', 'trip_id', 'bus_line_id','bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'bearing', 'status','created', 'updated' ], axis=1, inplace=True)

    # df['socket_date'] = pd.to_datetime(df['socket_date'])
    # df['socket_datetime'] = pd.to_datetime(df['socket_datetime'])
    # df['day_of_week'] = df['socket_date'].dt.dayofweek
    # df['hour'] = df['socket_datetime'].dt.hour
    # df['minute'] = df['socket_datetime'].dt.minute
    # df['second'] = df['socket_datetime'].dt.second
    df = df.drop(['index'], axis=1)
    df = df.reset_index()
    last_dt = date.today()
    for index, row in df.iterrows():
        print(index)
        check = False
        if row["direction"] == 3 or row['direction'] == 4:
            last_dt =  pd.to_datetime(row['socket_datetime'])
            df.at[index, 'time_taken'] = 0
        else:
            df.at[index, 'time_taken'] = int((pd.to_datetime(row['socket_datetime']) - last_dt).total_seconds())

    df.to_csv('../dataset/dataset_timeTaken/' + x  + '_timeTaken.csv', index=False)