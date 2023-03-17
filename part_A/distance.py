import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


fKulaiToLarkin = open('../dataset/KulaiToLarkin.json')
KulaiToLarkinData = json.load(fKulaiToLarkin)
fLarkinToKulai = open('../dataset/LarkinToKulai.json')
LarkinToKulaiData = json.load(fLarkinToKulai)

dataNames=['202105','202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201', '202202', '202203']
colNames=['socket_date', 'socket_datetime', 'lat', 'long', 'distance', 'speed', 'direction', 'busStop', 'time_taken','day_of_week','minuteOfDay']
for x in dataNames:
    df = pd.read_csv ('../dataset/part_A/dataset_minute/' + x + '_minute.csv', names=colNames, skiprows=1)
    df = df.reset_index()
    for index, row in df.iterrows():
        print(index)
        if row["direction"] == 1:
            for point in KulaiToLarkinData['stops']:
                if row['busStop'] == point['code']:
                    df.at[index, 'distanceToNext'] = point['distanceToNext']
                    break
        elif row["direction"] == 2:
            for point in LarkinToKulaiData['stops']:
                if row['busStop'] == point['code']:
                    df.at[index, 'distanceToNext'] = point['distanceToNext']
                    break

    df.to_csv('../dataset/part_A/dataset_distance/' + x + '_distance.csv', index=False)