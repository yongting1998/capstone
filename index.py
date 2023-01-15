import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

df = pd.read_csv ('./dataset/202105.csv', names=colNames, skiprows=1)
df["lat"] = df["lat"].str[1:].astype(float)
df["long"] = df["long"].str[:-1].astype(float)
# df = df[['lat', 'long']]
df = df[:10000]

last_station = ""
df = df.reset_index()
for index, row in df.iterrows():
    print(index)
    # kulai station
    if(abs(1.66246 - row["lat"]) < 2e-4 and abs(103.59879 - row["long"]) < 2e-4):
        last_station = "kulai"
        df.at[index, 'direction'] = "Kulai Station"
    
    # larkin station
    elif(abs(1.49534 - row["lat"]) < 2e-4 and abs(103.74262 - row["long"]) < 2e-4):
        last_station = "larkin"
        df.at[index, 'direction'] = "Larkin Station"
    else:
        #kulai to larkin -> 1
        #larkin to kulai -> 2
        if last_station == "kulai":
            df.at[index, 'direction'] = "1"
        if last_station == "larkin":
            df.at[index, 'direction'] = "2"

df.to_csv('test.csv', float_format='%.6f')

# df = df.reset_index()
# for index, row in df.iterrows():
#     print(index)
#     check = False
#     for point in KulaiToLarkinData:
#         if(abs(point[0] - row["long"]) < 1e-4 and abs(point[1] - row["lat"]) < 1e-4):
#             check = True
#             break
#     if not check:
#         df.drop(index, inplace=True)




# df = df.reset_index()
# for index, row in df.iterrows():
#     print(index)
#     if any(np.isclose(routeLat, row["lat"], atol=0.00001)):
#         if any(np.isclose(routeLong, row["long"], atol=0.00001)):
#             continue
#     else:
#         df.drop(index, inplace=True)



# df = df.reset_index()
# for index, row in df.iterrows():
#     print(index)
#     check = False
#     for point in routeLatLong:
#         if(abs(point[0] - row["long"]) < 1e-4 and abs(point[1] - row["lat"]) < 1e-4):
#             check = True
#             break
#     if not check:
#         df.drop(index, inplace=True)

  
# print(df['long'])

# plt.scatter(x=df['lat'], y=df['long'])
# plt.show()