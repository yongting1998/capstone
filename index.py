import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np

fLat = open('KulaiToLarkinLat.json')
routeLat = json.load(fLat)
fLong =  open('KulaiToLarkinLong.json')
routeLong = json.load(fLong)
fLatLong = open('KulaiToLarkinLatLongClean.json')
routeLatLong = json.load(fLatLong)

colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated']

df = pd.read_csv ('./dataset/202105.csv', names=colNames, skiprows=1)
df["lat"] = df["lat"].str[1:].astype(float)
df["long"] = df["long"].str[:-1].astype(float)
df = df[:30000]

# df = df.reset_index()
# for index, row in df.iterrows():
#     print(index)
#     if any(np.isclose(routeLat, row["lat"], atol=0.00001)):
#         if any(np.isclose(routeLong, row["long"], atol=0.00001)):
#             continue
#     else:
#         df.drop(index, inplace=True)



df = df.reset_index()
for index, row in df.iterrows():
    print(index)
    check = False
    for point in routeLatLong:
        if(abs(point[0] - row["long"]) < 1e-4 and abs(point[1] - row["lat"]) < 1e-4):
            check = True
            break
    if not check:
        df.drop(index, inplace=True)

  
# print(df['long'])

plt.scatter(x=df['lat'], y=df['long'])
plt.show()