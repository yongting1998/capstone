# capstone
capstone project

df["direction"]

0 = invalid
1 = Kulai to Larkin
2 = Larkin to Kulai
3 = Kulai Station
4 = Larkin Station

route #6 is Kulai To Larkin
route #7 is Larkin To Kulai

1. get direction first (dataset_direction)
2. get if points are on route (dataset_onRoute)
3. get bus stops and remove repeated bus stops, take depature only
4. get time taken from station to bus stop (seconds)
5. remove outliers (dataset_outlier)
6. get time of day(dataset_timeOfDay)
7. get time of day in minutes (dataset_minute)

extreme outliers found in 202203_time.csv
clean outliers with interquartile range
