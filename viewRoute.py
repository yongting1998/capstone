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