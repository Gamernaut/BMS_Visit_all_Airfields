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
import GreedyAlgorithm
import GeneticAlgorithm

debug_mode = False

# First read in all the airfields lat/log/alt values into a pandas dataframe
airfield_locations = pandas.read_csv('test_BMS_Airfield_Locations.csv')  # change to none test version

# Setup greedy algorithm instance
greedy_min_route = GreedyAlgorithm.MinimumContinuousRoute(airfield_locations)

# Now fill the dataframe with the distances from each airport to every other airport
greedy_min_route.calculate_airfield_distances()

if debug_mode:
    greedy_min_route.save_dataframe()

# Next start at the first airfield in the dataframe and work out the shortest route to every other airfield
# visiting each once but not returning to the start (not TSP problem). Do this for each airfield in the dataframe
print("\nRunning Minimal Continuous Route algorithm\n")
greedy_min_route.calculate_all_route_distances()
greedy_min_route.find_shortest_route()
greedy_min_route.print_shortest_route()

# Setup greedy algorithm instance with the number of iterations, defaults to 500
genetic = GeneticAlgorithm.GeneticOptimization(airfield_locations, 1000)

# Now fill the dataframe with the distances from each airport to every other airport
genetic.calculate_airfield_distances()

if debug_mode:
    genetic.save_dataframe()

# Next start at the first airfield in the dataframe and work out the shortest route to every other airfield
# visiting each once but not returning to the start (not TSP problem). Do this for each airfield in the dataframe
print("\n\nRunning Genetic Algorithm\n")
genetic.calculate_all_route_distances()
genetic.find_shortest_route()
genetic.print_shortest_route()
