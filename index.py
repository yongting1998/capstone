import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


fKulaiToLarkin = open('KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

df = pd.read_csv ('./dataset_onRoute/202202_onRoute.csv', names=colNames, skiprows=1)

# df = df[['lat', 'long']]
df = df[:10000]


df = df.reset_index()
count = 0
for index, row in df.iterrows():
    print(index)
    check = False
    for point in LarkinToKulaiData:
        if(abs(point[0] - row["lat"]) < 1e-4 and abs(point[1] - row["long"]) < 1e-4):
            check = True
            count+=1
            break
    if not check:
        df.drop(index, inplace=True)


plt.scatter(x=df['lat'], y=df['long'])
plt.show()
print ("count  " + str(count))


# df = df.reset_index()
# for index, row in df.iterrows():
#     print(index)
#     if any(np.isclose(routeLat, row["lat"], atol=0.00001)):
#         if any(np.isclose(routeLong, row["long"], atol=0.00001)):
#             continue
#     else:
#         df.drop(index, inplace=True)

  
# print(df['long'])
