import matplotlib.pyplot as plt
import pandas as pd
colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated']

df = pd.read_csv ('./dataset/202105.csv', names=colNames, skiprows=1)
df["lat"] = df["lat"].str[1:].astype(float)
df["long"] = df["long"].str[:-1].astype(float)
print(df['long'])

plt.scatter(x=df['lat'], y=df['long'])
plt.show()