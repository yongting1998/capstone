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
4. dataset get clean direction, sometimes bus u-turn halfway, only get full data from terminal to terminal

4. get time taken from station to bus stop (seconds)
5. remove outliers (dataset_outlier)
6. get time of day(dataset_timeOfDay)
7. get time of day in minutes (dataset_minute)


talk about the diff models
bus stop to bus stop
use distance as parameter


**cleaning data factors**
sometimes bus suddenly u-turn
sometimes does not end at terminal
gps faulty, sometimes don't capture points
sometimes bus starts halfway in the route
sometimes bus ends halfway today, starts next stop tomorrow (time taken calculated very long)
e.g. today end at 6030
tmrw start at 6031


**bullshit**

try different architecture for NN
try different activation functions (explain why this or that is better)
try different models
try different batch list and epoch
