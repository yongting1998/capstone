import matplotlib.pyplot as plt
import pandas as pd

colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated']

df = pd.read_csv ('./dataset/202110.csv', names=colNames, skiprows=1)
df["lat"] = df["lat"].str[1:].astype(float)
df["long"] = df["long"].str[:-1].astype(float)



last_station = ""
df = df.reset_index()
for index, row in df.iterrows():
    print(index)
    # kulai station
    if(abs(1.66246 - row["lat"]) < 2e-4 and abs(103.59879 - row["long"]) < 2e-4):
        last_station = "kulai"
        df.at[index, 'direction'] = 3
    
    # larkin station
    elif(abs(1.49534 - row["lat"]) < 2e-4 and abs(103.74262 - row["long"]) < 2e-4):
        last_station = "larkin"
        df.at[index, 'direction'] = 4
    else:
        #kulai to larkin -> 1
        #larkin to kulai -> 2
        if last_station == "kulai":
            df.at[index, 'direction'] = 1
        if last_station == "larkin":
            df.at[index, 'direction'] = 2
        else:
            df.at[index, 'direction'] = 0

df["direction"] = df["direction"].astype(int)
df.to_csv('./dataset_direction/202110_direction.csv')