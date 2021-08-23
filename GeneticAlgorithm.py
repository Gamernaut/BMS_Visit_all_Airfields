#######################################################################################################################
#
#   Author:         Carmelo Volpe
#
#   Date:           August 2021

#   Description:    Encapsulates the search algorithm to find the shortest route, in miles, of visiting
#                   every airfield in the input file at least once but not returning to the start airfield
#                   (not the same as the classic travelling salesman problem). Uses a Genetic algorithm approach
#                   to generate a number of routes to optimise around. Checking all combinations is a factorial
#                   expansion, the 48 airfields north of the DMZ in Falcon BMS would mean checking 1.2E61
#                   combinations.
#
#                   The algorithm follows the standard Genetic Algorithm flow of creating a population, selecting the
#                   "fittest", mating and mutating then generating the offspring generation. This then goes through the
#                   whole process again for the specified number of generations. The fitness function is a simple
#                   distance measure (the longer the distance the worse the fit).
#
#######################################################################################################################

import sys
import numpy
import random
import operator
import pandas

from Utility_Functions import haversine_distance, load_dataframe


class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    # rewrite to use dataframe for source of info (access distance at cell position df.at[from_airfield,to_airfield]
    def route_distance(self):
        if self.distance == 0:
            route_distance = 0
            for i in range(0, len(self.route)):
                from_airfield = self.route[i]
                to_airfield = self.route[i + 1]
                route_distance += from_airfield.distance(to_airfield)
            self.distance = route_distance
        return self.distance

    def route_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.route_distance())
        return self.fitness


class GeneticOptimization:
    def __init__(self, filename, population_size=100, elite_size=20, mutation_rate=0.01, generations=500):
        self.input_data_file = filename
        self.airfields_df = load_dataframe(self.input_data_file)
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations
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
        del self.airfields_df['Lat']
        del self.airfields_df['Long']
        del self.airfields_df['Altitude']

    def create_initial_population(self):
        population = []

        for i in range(0, self.population_size):
            route = random.sample(self.airfields_df['Airfields'], self.airfield_count)
            population.append(route)
        return population

    def rank_routes(self, current_generation):
        fitness_results = {}
        for i in range(0, len(current_generation)):
            fitness_results[i] = Fitness(current_generation[i]).routeFitness()
        return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)

    def select_best_routes(self, ranked_routes):
        selection_results = []
        df = pandas.DataFrame(numpy.array(ranked_routes), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        for i in range(0, self.elite_size):
            selection_results.append(ranked_routes[i][0])
        for i in range(0, len(ranked_routes) - self.elite_size):
            pick = 100 * random.random()
            for i in range(0, len(ranked_routes)):
                if pick <= df.iat[i, 3]:
                    selection_results.append(ranked_routes[i][0])
                    break
        return selection_results

    def breed(self, parent1, parent2):
        child = []
        childP1 = []
        childP2 = []

        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(startGene, endGene):
            childP1.append(parent1[i])

        childP2 = [item for item in parent2 if item not in childP1]

        child = childP1 + childP2
        return child

    def breed_population(self, mating_pool):
        children = []
        length = len(mating_pool) - self.elite_size
        pool = random.sample(mating_pool, len(mating_pool))

        for i in range(0, self.elite_size):
            children.append(mating_pool[i])

        for i in range(0, length):
            child = self.breed(pool[i], pool[len(mating_pool) - i - 1])
            children.append(child)
        return children

    def create_mating_pool(self, current_generation, selected_routes):
        mating_pool = []
        for i in range(0, len(selected_routes)):
            index = selected_routes[i]
            mating_pool.append(current_generation[index])
        return mating_pool

    def mutate(self, individual):
        for swapped in range(len(individual)):
            if random.random() < self.mutation_rate:
                swap_with = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swap_with]

                individual[swapped] = city2
                individual[swap_with] = city1
        return individual

    def mutate_population(self, population):
        mutated_population = []

        for ind in range(0, len(population)):
            mutated_individual = self.mutate(population[ind])
            mutated_population.append(mutated_individual)
        return mutated_population

    def create_next_generation(self, current_generation):
        ranked_routes = self.rank_routes(current_generation)
        selected_routes = self.select_best_routes(ranked_routes)
        mating_pool = self.create_mating_pool(current_generation, selected_routes)
        children = self.breed_population(mating_pool)
        next_generation = self.mutate_population(children)
        return next_generation

    def find_shortest_route(self, ):
        # create initial population
        current_population = self.create_initial_population()

        # call next generation
        for i in range(0, self.generations):
            current_population = self.create_next_generation(current_population)

    def print_shortest_route(self):
        pass

    def save_dataframe(self):
        self.airfields_df.to_csv('dataframe_distances_gen_algo.csv')
