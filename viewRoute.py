import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np

fLatLong = open('KulaiToLarkin.json')
routeLatLong = json.load(fLatLong)
x = []
y = []
for points in routeLatLong:
    for z in points:
        if z < 90:
            x.append(z)
        else:
            y.append(z)
plt.scatter(x,y)
plt.show()
            
# colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

# df = pd.read_csv ('./dataset_onRoute/202202_onRoute.csv', names=colNames, skiprows=1)
# plt.scatter(x=df['lat'], y=df['long'])
# plt.show()

