District, starting time, ending time, total days, and total budget are collected from the user. All places in the district are retrieved from the database and sorted according to their weighted rating.

Calculating the weighted rating:
    The weighted rating for a place is calculated based on its rating, reviews, and the maximum review in the database. The equation for the weighted rating is 
    (1/(1+exp((-reviews*10)/MAXIMUM_REVIEWS)))*rating
    
Till the schedule for the trip fits the available time, we remove places one by one in each iteration such that the removed place will be having the least weighted rating among the places. The distance matrix is calculated and the algorithm for route generation is called by the matrix as the parameters. The output of the algorithm will be a linked list containing the order in which the places are to be visited.

Calculating Distance matrix:
    The algorithm uses Haversine formula which returns the shortest distance between two geographical coordinates. The distance between two places is taken as their straight line distance.
    The output is a 2D square matrix with each element being the shortest or the straight line distance between 2 location coordinates in Kilometers.
    
    
 The distance matrix, place visit order, total days, starting time, ending time, and total budget are passed as the parameters to the schedule generating function. The function accepts car as the default travelling mode. To adjust the budget the algorithm assumes that if the mode of traveling is car then for every 25 Kilometers traveled a cost of 70 is deducted from the available budget. The function splits the place visit order into days by grouping all the places that could be visited on a single day. If no more places could be visited on a day because of time constraints on that day then the place will be added to the next day's schedule. If no more places could be visited because of the budget or if no more places left then the algorithm stops running thereby returning the schedule for the trip. 
 
The output of the schedule generating function will be an array with each element containing the duration, place name as the value. This output will be accepted only if the length of the array, which indicates the number of days it will take to create a trip with all these places, is less than or equal to the total days the user is going to spent else the schedule does not fit so the algorithm starts again by poping the least rated place as mentioned above.

The accepted output will be displayed to the user in the format
<DAY 1>
<Start Time - End Time> <Place Name>
<Start Time - End Time> <Place Name>
<Start Time - End Time> <Place Name>

<DAY 2>
<Start Time - End Time> <Place Name>
<Start Time - End Time> <Place Name>
<Start Time - End Time> <Place Name>
.
.
.



