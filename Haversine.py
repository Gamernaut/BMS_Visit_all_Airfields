###########################################################################################
#
#   Author:     Carmelo Volpe
#
#   Date:       August 2021
#
#   Usage:      Used by main script Find_Shortest_Flight.py
#
#   This File:  Uses the Haversine formula to calculate the distance in miles between the
#               2 input pairs of longitude and latitude. It returns the distance
#               in miles. Does not account for height differences.
#
#   Usage:      distance = haversine_distance([longitude1, latitude1],[longitude2, latitude2])
#
###########################################################################################

import math

''' Uses Haversine formula to calculate the distance between 2 Latitude/Longitude coordinates in miles.
@inputs - 2 tuples each of which represents a pair of Latitudinal and Longitudinal values as decimals
@returns - the distance between them in miles '''


def haversine_distance(location1, location2):
    lat1, lon1 = location1
    lat2, lon2 = location2

    earth_radius = 3958.8         # Radius of earth in miles
    # earth_radius = 3440.1  # Radius of earth in miles
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius * c
