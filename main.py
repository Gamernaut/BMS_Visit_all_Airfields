###########################################################################################
#
#   Author:     Carmelo Volpe
#
#   Date:       August 2021
#
#   This File:
#
#   Usage:
#
###########################################################################################

import pandas
from Haversine import haversine_distance

# First read in all the airfields lat/log/alt values into a pandas dataframe
airfield_locations = pandas.read_csv('test_BMS_Airfield_Locations.csv')  # change to none test version

# Loop through each row. Take the name of the airfield and create a list which has the airfield name at the top and
# each cell contains the distance from each airfield to the one in the title = 2D matrix of distances
for i in airfield_locations.index:
    haversine_distances_list = []  # holds the calculated distances to add to the dataframe later
    coord1 = [airfield_locations.at[i, 'Lat'], airfield_locations.at[i, 'Long']]
    for j in airfield_locations.index:
        coord2 = [airfield_locations.at[j, 'Lat'], airfield_locations.at[j, 'Long']]
        distance = haversine_distance(coord1, coord2)
        haversine_distances_list.append(round(distance, 3))
    airfield = airfield_locations.at[i, 'Airfield']
    # Add a new column of distances to the dataframe under the airfield name
    airfield_locations[airfield] = haversine_distances_list

# write dataframe to file for manual checking code
airfield_locations.to_csv('dataframe_distances.csv')

airfield_count = airfield_locations['Airfield'].count()
total_distance = 0.0
list_of_routes = []
# Per row in input file loop
for row in airfield_locations.index:
    current_airfield = airfield_locations.at[row, 'Airfield']
    current_route = [[current_airfield, 0.0]]
    # Per distances in a column for a specific airfield loop
    for count in range(airfield_count - 1):
        distances = airfield_locations.reset_index()[['Airfield', current_airfield]].values.tolist()
        best_distance = 1000
        best_airfield = ''
        for airfield, distance in distances:
            if not any(airfield in sl for sl in current_route):  # exclude airfields already in the list (the
                # one added in the last loop will be closest) avoids endless loop
                if float(distance) < best_distance and float(distance) > 0:
                    best_distance = float(distance)
                    best_airfield = airfield
        current_route.append([best_airfield, best_distance])
        current_airfield = best_airfield
    list_of_routes.append(current_route)

shortest_dist = 100000.0
shortest_route = []
for route in list_of_routes:
    for element in route:
        total_distance = total_distance + element[1]
    if total_distance < shortest_dist:
        shortest_dist = total_distance
        shortest_route = route
    total_distance = 0

print(f'Shortest route is {shortest_dist:4.1f} miles\n')
steerpoint = 1
for airfield in shortest_route:
    name = airfield[0]
    miles = airfield[1]
    print(f'Steerpoint {steerpoint} is {str(name)} which is {miles} miles from previous steerpoint')
    # print(airfield)
    steerpoint += 1
