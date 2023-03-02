import pandas as pd


# dataNames=['202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112', '202201','202202','202203']
dataNames=['202203']
for x in dataNames:
    print(x)
    colNames=['id', 'trip_id', 'bus_line_id', 'socket_date', 'socket_datetime', 'lat', 'long', 'bus_vehicle_id', 'bus_plate', 'station_id', 'station_code', 'distance', 'speed', 'bearing', 'status','created', 'updated','direction','day_of_week','hour','minute','second']

    df = pd.read_csv ('./dataset_day/' + x + '_day.csv', names=colNames, skiprows=1)
    #dfTerminals = df.loc[df['direction'] > 2]
    #remove previous row if value is same
    #sometimes bus is at terminal for a long time
    #dfTerminals = dfTerminals[~dfTerminals.filter(like='direction').diff().eq(0).all(1)]
    dfTerminals = df
    dfTerminals = dfTerminals[~((dfTerminals['direction'] == dfTerminals['direction'].shift(-1)) & (dfTerminals['direction'] > 2))]
    print(dfTerminals)