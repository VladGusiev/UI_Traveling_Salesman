# GENETIC ALGORITHM
import copy
import math

import matplotlib.pyplot as plt
import random

POPULATION_AMOUNT = 20
# CITIES_ARRAY = []


# Initial generation of cities
def generate_cities():
    cities_array = []
    for i in range(random.randrange(20, 40)):
        cities_array.append([random.randrange(200), random.randrange(200)])
    # print(cities_array)
    return cities_array


# Generation of 1. generation (randomly shuffled list of cities)
def generate_first_generation(list_of_cities):
    new_generation = []
    for _ in range(20):
        random.shuffle(list_of_cities)  # does not return anything
        new_generation.append(Individual(copy.deepcopy(list_of_cities)))
    return new_generation


class Individual:
    def __init__(self, chromosomes):
        self.chromosomes = chromosomes
        self.fitness = self.detectFitness()


    def detectFitness(self):
        # TODO calculate length of road by pythagoras theorem
        total_length = 0

        for i in range(1, len(self.chromosomes)):
            x1, y1 = self.chromosomes[i - 1]
            x2, y2 = self.chromosomes[i]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_length += distance

        return 1/total_length # closer number to 1 -> shorter road!


def main(points_array):
    population = generate_first_generation(points_array)
    for i in range(len(population)):
        x, y = zip(*population[i].chromosomes)  # Unzip the points into separate x and y arrays
        plt.clf()  # Clear the current figure
        plt.plot(x, y, marker='o', linestyle='solid')
        plt.xlabel('X-Axis')
        plt.ylabel('Y-Axis')
        plt.title('Traveling Salesman')
        plt.grid(True)

        plt.show()


if __name__ == '__main__':

    # input_array = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]
    input_array = generate_cities()
    main(input_array)

