###########################################################################################
#
#   Author:         Carmelo Volpe
#
#   Date:           August 2021
#
#   Description:    Encapsulates the search algorithm
#
#   This File:
#
###########################################################################################

import sys
from Haversine import haversine_distance


class GeneticOptimization:
    def __init__(self, airfield_dataframe=None, iterations=500):
        self.airfields_df = airfield_dataframe
        self.iterations = iterations
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
       pass

    def find_shortest_route(self):
        pass

    def print_shortest_route(self):
        print(f'\n\nShortest route is {self.shortest_dist:4.1f} miles')
        steerpoint = 1
        for airfield in self.shortest_route:
            name = airfield[0]
            miles = airfield[1]
            print(f'\tSteerpoint {steerpoint} is {str(name)} which is {miles} miles from previous steerpoint')
            # print(airfield)
            steerpoint += 1

    def save_dataframe(self):
        self.airfields_df.to_csv('dataframe_distances_gen_algo.csv')
