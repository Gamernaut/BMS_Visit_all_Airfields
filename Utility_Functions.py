###########################################################################################
#
#   Author:     Carmelo Volpe
#
#   Date:       August 2021
#
#   This File:  Uses the Haversine formula to calculate the distance in miles between the
#               2 input pairs of longitude and latitude. It returns the distance
#               in miles. Does not account for height differences.
#
#   Usage:      distance = haversine_distance([longitude1, latitude1],[longitude2, latitude2])
#
###########################################################################################

import math
import pandas

"""
Uses Haversine formula to calculate the distance between 2 Latitude/Longitude coordinates in miles accounting
    for the curvature of the earth.
    
    Haversine formula:	a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    
    c = 2 ⋅ atan2( √a, √(1−a) )
    d = R ⋅ c
    
    where φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
    All angles need to be in radians    
    
@inputs - 2 tuples each of which represents a pair of Latitudinal and Longitudinal values as decimals
@returns - the distance between the pair of input coordinates in miles
"""

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


"""
Read in the contents of the file and create a dataframe with just the data needed for the algorithms

@inputs - filename containing airfield data
@returns - the correctly formatted dataframe for use in the algorithms
"""

def load_dataframe(filename):
    # First read in all the airfields lat/log/alt values into a pandas dataframe
    return pandas.read_csv(filename)
