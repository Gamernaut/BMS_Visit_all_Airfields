###########################################################################################
#
#   Author:         Carmelo Volpe
#
#   Date:           August 2021
#
#   Description:    Encapsulates the search algorithm to find the shortest route, in miles, visiting every airfield
#                   in the input file at least once but not returning to the start airfield (not the same as the
#                   classic travelling salesman problem). Uses a Greedy algorithm approach by focusing on the next
#                   closest airfield to the current one. May not be globally optimal but checking all combinations
#                   is a factorial expansion, the 48 airfields north of the DMZ in Falcon BMS would mean checking
#                   1.2E61 combinations.
#
#                   The algorithm starts at the first airfield in the input file and then finds the closest airfield.
#                   It adds this to the route and then uses this airfield as the current airfield and finds the
#                   next nearest. Once it has visited every airfield once, it then moves on to the next airfield
#                   in the file and repeats the process. The result is a 2D array/list of lists of the shortest
#                   routes starting from every airfield in the input file.
#
###########################################################################################

import pandas
import GreedyAlgorithm
import GeneticAlgorithm

debug_mode = False

# Create Greedy Algorithm instance
greedy_min_route = GreedyAlgorithm.MinimumContinuousRoute('test_BMS_Airfield_Locations.csv')

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
genetic = GeneticAlgorithm.GeneticOptimization('test_BMS_Airfield_Locations.csv', generations=1000)

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
