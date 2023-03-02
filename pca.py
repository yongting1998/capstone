import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction']

df = pd.read_csv ('./dataset_onRoute/202110_onRoute.csv', names=colNames, skiprows=1)

df = df.drop(['socket_date','socket_datetime','id', 'trip_id','bus_line_id','bus_vehicle_id','bus_plate', 'station_id','station_code', 'status', 'created', 'updated'], axis=1)


df['distance'] = df['distance'].apply(lambda x: float(x.split()[0].replace("'", '')))
df['speed'] = df['speed'].apply(lambda x: float(x.split()[0].replace("'", '')))
df['bearing'] = df['bearing'].apply(lambda x: float(x.split()[0].replace("'", '')))



numComponents = 4
pca = PCA(n_components=numComponents)
pca.fit(df)
projected = pca.transform(df)

tot = sum(pca.explained_variance_)
print(pca.explained_variance_)
print(tot)

var_exp = [(i / tot) for i in sorted(pca.explained_variance_, reverse=True)]
cum_var_exp = np.cumsum(var_exp)
print(len(var_exp))
# plot explained variances
plt.bar(range(1,5), var_exp, alpha=0.5,
        align='center', label='individual explained variance')
plt.step(range(1,5), cum_var_exp, where='mid',
         label='cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal component index')
plt.legend(loc='best')
plt.show()