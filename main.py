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
import sys
from Haversine import haversine_distance

debug_mode = True

def calculate_distances():
    """Loops through each airfield in the data frames first column and adds a column to the dataframe.
    This column contains the Haversine distance, calculated using the imported function, from this airfield (in the
    column label) to each of the other airfields in the file. Ultimately the dataframe contains the distance from
    every airfield to every other airfield"""
    # Loop through each row. Take the name of the airfield and create a list which has the airfield name at the
    # top and each cell contains the distance from each airfield to the one in the title = 2D matrix of distances
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


def calculate_all_route_distances():
    global total_distance, list_of_routes, count, airfield
    airfield_count = airfield_locations['Airfield'].count() - 1
    total_distance = 0.0
    list_of_routes = []
    # Per row in input file loop
    for row in airfield_locations.index:
        current_airfield = airfield_locations.at[row, 'Airfield']
        current_route = [[current_airfield, 0.0]]
        # Per distances in a column for a specific airfield loop
        pct_complete = (row / airfield_count) * 100
        sys.stdout.write(f"\rProcessing airfields : %d%% completed - Currently processing {current_airfield}"
                         % pct_complete)  # Prints on the same line
        for count in range(airfield_count):
            distances = airfield_locations.reset_index()[['Airfield', current_airfield]].values.tolist()
            best_distance = 1000
            best_airfield = ''
            for airfield, distance in distances:
                if not any(airfield in sl for sl in current_route):  # exclude airfields already in the list (the
                    # one added in the last loop will be closest) avoids endless loop
                    # line below is equivalent to float(distance) < best_distance and float(distance) > 0
                    if best_distance > float(distance) > 0:
                        best_distance = float(distance)
                        best_airfield = airfield
            current_route.append([best_airfield, best_distance])
            current_airfield = best_airfield
        list_of_routes.append(current_route)


def find_shortest_route():
    global shortest_dist, shortest_route, total_distance
    shortest_dist = 100000.0
    shortest_route = []
    for route in list_of_routes:
        for element in route:
            total_distance = total_distance + element[1]
        if total_distance < shortest_dist:
            shortest_dist = total_distance
            shortest_route = route
        total_distance = 0
    return shortest_route


def print_shortest_route():
    global airfield
    print(f'\n\nShortest route is {shortest_dist:4.1f} miles\n')
    steerpoint = 1
    for airfield in shortest_route:
        name = airfield[0]
        miles = airfield[1]
        print(f'Steerpoint {steerpoint} is {str(name)} which is {miles} miles from previous steerpoint')
        # print(airfield)
        steerpoint += 1


# First read in all the airfields lat/log/alt values into a pandas dataframe
airfield_locations = pandas.read_csv('test_BMS_Airfield_Locations.csv')  # change to none test version

# Now fill the dataframe with the distances from each airport to every other airport
calculate_distances()

# For manual checking of distance calculations write dataframe to file
if debug_mode:
    airfield_locations.to_csv('dataframe_distances.csv')

# Next start at the first airfield in the dataframe and work out the shortest route to every other airfield
# visiting each once but not returning to the start (not TSP problem). Do this for each airfield in the dataframe
print("Running Greedy Algorithm")
calculate_all_route_distances()
shortest_route = find_shortest_route()
print_shortest_route()
