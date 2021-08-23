#######################################################################################################################
#
#   Author:         Carmelo Volpe
#
#   Date:           August 2021
#
#   Description:    Encapsulates the search algorithm to find the shortest route, in miles, of visiting
#                   every airfield in the input file at least once but not returning to the start airfield
#                   (not the same as the classic travelling salesman problem). Uses a Greedy algorithm approach
#                   by focusing on the next closest airfield to the current one. May not be globally optimal
#                   but checking all combinations is a factorial expansion, the 48 airfields north of the DMZ
#                   in Falcon BMS would mean checking 1.2E61 combinations.
#
#                   The algorithm starts at the first airfield in the input file and then finds the closest airfield.
#                   It adds this to the route and then uses this airfield as the current airfield and finds the
#                   next nearest. Once it has visited every airfield once, it then moves on to the next airfield
#                   in the file and repeats the process. The result is a 2D array/list of lists of the shortest
#                   routes starting from every airfield in the input file.
#
#######################################################################################################################

import sys
import time
from Utility_Functions import haversine_distance
from Utility_Functions import load_dataframe


class MinimumContinuousRoute:
    def __init__(self, filename):
        self.data_input_file = filename
        self.airfields_df = load_dataframe(self.data_input_file)
        self.total_distance = 0.0
        self.list_of_routes = []
        self.airfield_count = self.airfields_df['Airfield'].count() - 1
        self.shortest_dist = 100000.0
        self.shortest_route = []

    def calculate_airfield_distances(self):
        """Loops through each airfield in the data frames first column and adds a column to the dataframe.
        This column contains the Haversine distance, calculated using the imported function, from this airfield (in the
        column label) to each of the other airfields in the file. Ultimately the dataframe contains the distance from
        every airfield to every other airfield"""
        # Loop through each row. Take the name of the airfield and create a list which has the airfield name at the
        # top and each cell contains the distance from each airfield to the one in the title = 2D matrix of distances
        for i in self.airfields_df.index:
            haversine_distances_list = []  # holds the calculated distances to add to the dataframe later
            coord1 = [self.airfields_df.at[i, 'Lat'], self.airfields_df.at[i, 'Long']]
            for j in self.airfields_df.index:
                coord2 = [self.airfields_df.at[j, 'Lat'], self.airfields_df.at[j, 'Long']]
                distance = haversine_distance(coord1, coord2)
                haversine_distances_list.append(round(distance, 3))
            airfield = self.airfields_df.at[i, 'Airfield']
            # Add a new column of distances to the dataframe under the airfield name
            self.airfields_df[airfield] = haversine_distances_list

    def calculate_all_route_distances(self):
        """ Simple algorithm which starts at an airfield and then looks for the next nearest excluding any that
         have already been visited """
        start_time = time.perf_counter()
        # Per row in input file loop
        for row in self.airfields_df.index:
            current_airfield = self.airfields_df.at[row, 'Airfield']
            current_route = [[current_airfield, 0.0]]
            # Per distances in a column for a specific airfield loop
            pct_complete = (row / self.airfield_count) * 100
            estimated_secs_remaining = ((time.perf_counter() - start_time)/(row + 1)) * (self.airfield_count - row)
            sys.stdout.write(f"\rProcessing airfields : %d%% completed - Time remaining {estimated_secs_remaining:3.3}"
                             f" seconds" % pct_complete)  # Prints on the same line
            for count in range(self.airfield_count):
                distances = self.airfields_df.reset_index()[['Airfield', current_airfield]].values.tolist()
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
            self.list_of_routes.append(current_route)

    def find_shortest_route(self):
        """Adds up the distances in each route, keeping a track of which is the shortest so far"""
        total_distance = 0.0
        for route in self.list_of_routes:
            for element in route:
                total_distance = total_distance + element[1]
            if total_distance < self.shortest_dist:
                self.shortest_dist = total_distance
                self.shortest_route = route
            total_distance = 0.0

    def print_shortest_route(self):
        """Prints out the shortest route in a more human friendly format than just displaying the list"""
        print(f'\n\nShortest route is {self.shortest_dist:4.1f} miles')
        steerpoint = 1
        for airfield in self.shortest_route:
            name = airfield[0]
            miles = airfield[1]
            print(f'\tSteerpoint {steerpoint} is {str(name)} which is {miles} miles from previous steerpoint')
            # print(airfield)
            steerpoint += 1

    def save_dataframe(self):
        """Saves the dataframe to a .csv file. Usually called after the dataframe has been populated with all the
        Haversine distances between every airfield so that the algorithm can be checked manually"""
        self.airfields_df.to_csv('dataframe_distances_MCR_algo.csv')
