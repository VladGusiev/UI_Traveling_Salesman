import copy
import math
import time

import matplotlib.pyplot as plt
import random

CITIES_NUMBER = 0  # will be set in generate_cities()


def generate_cities():
    cities_array = []
    global CITIES_NUMBER
    CITIES_NUMBER = random.randrange(20, 40)
    # CITIES_NUMBER = random.randrange(10, 11)
    for i in range(CITIES_NUMBER):
        cities_array.append([random.randrange(200), random.randrange(200)])
    print(cities_array)
    print("START RESULT")
    x, y = zip(*cities_array)  # Unzip the points into separate x and y arrays
    x = list(x) + [x[0]]
    y = list(y) + [y[0]]
    plt.plot(x, y, marker='o', linestyle='solid')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Traveling Salesman Genetic Algorithm')
    plt.grid(True)
    plt.show()
    return cities_array


class Individual:
    def __init__(self, cities_array):
        self.cities_array = cities_array
        self.fitness = self.calculate_fitness()

    # calculate fitness of individual
    def calculate_fitness(self):
        # TODO calculate length of road by pythagoras theorem
        total_length = 0

        for i in range(1, len(self.cities_array)):
            x1, y1 = self.cities_array[i - 1]
            x2, y2 = self.cities_array[i]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_length += distance
        first_and_last_cite_distance = math.sqrt((self.cities_array[0][0] - self.cities_array[-1][0]) ** 2 + (self.cities_array[0][1] - self.cities_array[-1][1]) ** 2)
        total_length += first_and_last_cite_distance

        return 1/total_length  # closer number to 1 -> shorter road!

def generate_neighborhoods(current_permutation):
    neighborhoods = []
    for i in range(len(current_permutation.cities_array)):
        for j in range(i + 1, len(current_permutation.cities_array)):
            new_permutation = copy.deepcopy(current_permutation)
            new_permutation.cities_array[i], new_permutation.cities_array[j] = new_permutation.cities_array[j], new_permutation.cities_array[i]
            new_permutation.fitness = new_permutation.calculate_fitness()  # recalculating fitness
            neighborhoods.append(new_permutation)
    return neighborhoods

def find_best_neighborhood(neighborhoods):
    best_neighborhood = neighborhoods[0]
    for neighborhood in neighborhoods:
        if neighborhood.fitness > best_neighborhood.fitness:
            best_neighborhood = neighborhood
    return best_neighborhood


def main(points_array):
    current_permutation = Individual(copy.deepcopy(points_array))  # initial permutation of cities

    found = False
    iteration = 1
    convergence_counter = 1000

    all_time_best_permutation = copy.deepcopy(current_permutation)

    taboo_list = [current_permutation]

    while not found:

        if convergence_counter <= 0:
            found = True
            break

        # generate neighborhoods
        neighborhoods = generate_neighborhoods(current_permutation)

        # find best neighborhood
        best_neighborhood = find_best_neighborhood(neighborhoods)

        # check if best neighborhood is in taboo list
        while best_neighborhood in taboo_list:
            if len(neighborhoods) == 1:
                neighborhoods = generate_neighborhoods(current_permutation)
                best_neighborhood = find_best_neighborhood(neighborhoods)
                break
            # if yes, remove it and find new best neighborhood
            neighborhoods.remove(best_neighborhood)
            best_neighborhood = neighborhoods[0]
            for neighborhood in neighborhoods:
                if neighborhood.fitness > best_neighborhood.fitness:
                    best_neighborhood = neighborhood

        # check if best neighborhood is better than current permutation
        if best_neighborhood.fitness > current_permutation.fitness:
            current_permutation = copy.deepcopy(best_neighborhood)
            # check if best neighborhood is better than all time best permutation
            if best_neighborhood.fitness > all_time_best_permutation.fitness:
                all_time_best_permutation = copy.deepcopy(best_neighborhood)
                convergence_counter = 1000
            else:
                convergence_counter -= 1

        if best_neighborhood.fitness < current_permutation.fitness:
            taboo_list.append(current_permutation)
            if len(taboo_list) > 50:
                taboo_list.pop(0)
            current_permutation = copy.deepcopy(best_neighborhood)

        iteration += 1


    print(
        f"Generation: {iteration}\tString: {all_time_best_permutation.cities_array}\tFitness: {all_time_best_permutation.fitness}")
    x, y = zip(*current_permutation.cities_array)
    # connect first and last point of the graph
    x = list(x) + [x[0]]
    y = list(y) + [y[0]]
    plt.plot(x, y, marker='o', linestyle='solid')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Traveling Salesman Taboo Search')
    plt.grid(True)
    plt.show()
    plt.pause(0.05)


if __name__ == '__main__':
    input_array = generate_cities()
    main(input_array)