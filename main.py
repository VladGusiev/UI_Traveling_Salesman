# GENETIC ALGORITHM
import copy
import math
import time

import matplotlib.pyplot as plt
import random

POPULATION_AMOUNT = 500
CITIES_NUMBER = 0  # will be set in generate_cities()
# CITIES_ARRAY = []


# Initial generation of cities
def generate_cities():
    cities_array = []
    global CITIES_NUMBER
    CITIES_NUMBER = random.randrange(20, 40)
    # CITIES_NUMBER = random.randrange(10, 11)
    for i in range(CITIES_NUMBER):
        cities_array.append([random.randrange(200), random.randrange(200)])

    # print(cities_array)
    # random.shuffle(cities_array)
    # print(cities_array)
    return cities_array


# Generation of 1. generation (randomly shuffled list of cities)
def generate_first_generation(list_of_cities):
    new_generation = []
    for _ in range(POPULATION_AMOUNT):
        random.shuffle(list_of_cities)  # does not return anything
        new_generation.append(Individual(copy.deepcopy(list_of_cities)))

    # print(new_generation)
    # print(len(new_generation))

    return new_generation


class Individual:
    def __init__(self, chromosomes):
        self.chromosomes = chromosomes
        self.fitness = self.detect_fitness()

    def detect_fitness(self):
        # TODO calculate length of road by pythagoras theorem
        total_length = 0

        for i in range(1, len(self.chromosomes)):
            x1, y1 = self.chromosomes[i - 1]
            x2, y2 = self.chromosomes[i]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_length += distance
        first_and_last_cite_distance = math.sqrt((self.chromosomes[0][0] - self.chromosomes[-1][0]) ** 2 + (self.chromosomes[0][1] - self.chromosomes[-1][1]) ** 2)
        total_length += first_and_last_cite_distance

        return 1/total_length  # closer number to 1 -> shorter road!

    # MUTATION -> switching 2 genes
    def mutate(self):
        mutation_type = random.randrange(1, 3, 1)

        #  switch genes next to each other
        if mutation_type == 1:
            #                                      inc          not incl
            mutated_gene = random.randrange(1, len(self.chromosomes))
            self.chromosomes[mutated_gene], self.chromosomes[mutated_gene - 1] = self.chromosomes[mutated_gene - 1], self.chromosomes[mutated_gene]

        #  switch 2 random genes
        elif mutation_type == 2:
            first_gene = random.randrange(len(self.chromosomes))
            second_gene = random.randrange(len(self.chromosomes))
            while second_gene == first_gene:
                second_gene = random.randrange(len(self.chromosomes))
            self.chromosomes[first_gene], self.chromosomes[second_gene] = self.chromosomes[second_gene], self.chromosomes[first_gene]

    def get_new_blood(self):
        randomised_chromosomes = copy.deepcopy(self.chromosomes)
        random.shuffle(randomised_chromosomes)  # does not return anything
        return randomised_chromosomes

    def create_offspring(self, par2):

        # chromosome for offspring
        child_chromosome = []

        new_blood_chance = random.random()
        # chance to create new blood
        if new_blood_chance <= 0.1:
            # print(self.get_new_blood())
            child_chromosome = copy.deepcopy(self.get_new_blood())
        else:
            # for gp1, gp2 in zip(self.chromosomes, par2.chromosomes):
            max_cutout_size = int(CITIES_NUMBER / 2)
            cutout_size = random.randrange(1, max_cutout_size)
            # print(len(self.chromosomes))

            cut_out_place = random.randrange(len(self.chromosomes) - cutout_size + 1)
            inherited_part = copy.deepcopy(self.chromosomes[cut_out_place:cut_out_place + cutout_size])
            # print(f"size: {cutout_size}, place: {cut_out_place}, output: {inherited_part}")
            inherited_part.reverse()

            for gene in par2.chromosomes:
                if gene not in inherited_part:
                    child_chromosome.append(gene)
            for i in range(cutout_size):
                child_chromosome.insert(cut_out_place, inherited_part[i])

        return Individual(child_chromosome)


def roulette_selection(population):
    total_fitness = sum(chromosome.fitness for chromosome in population)
    selected_fitness = random.uniform(0, total_fitness)
    current_sum_of_fitness = 0

    for i, chromosome in enumerate(population):
        current_sum_of_fitness += chromosome.fitness
        if current_sum_of_fitness > selected_fitness:
            return copy.deepcopy(population[i])


def main(points_array):
    population = generate_first_generation(points_array)
    generation = 1
    found = False
    convergence_counter = 2500
    all_time_best_fit = 0
    new_generation = []
    while not found:

        # sort the population in decreasing order of fitness score
        population = sorted(population, key=lambda x: x.fitness, reverse=True)

        if convergence_counter <= 0:
            found = True
            break
        # Otherwise generate new offsprings for new generation
        new_generation = []

        new_parents_amount = int((10 * POPULATION_AMOUNT) / 100)  # 10% of population

        choice_of_parent_method = random.randrange(1, 3, 1)
        if choice_of_parent_method == 1:
        #  ----------- RULETTE ------------------------
        # total_fitness = sum(chromosome.fitness for chromosome in population)
        # for _ in range(new_parents_amount):
        #     selected_fitness = random.uniform(0, total_fitness)
        #     current_sum_of_fitness = 0
        #
        #     for i, chromosome in enumerate(population):
        #         current_sum_of_fitness += chromosome.fitness
        #         if current_sum_of_fitness > selected_fitness:
        #             new_generation.append(copy.deepcopy(population[i]))
        #             break
            parents_for_next_generation = []
            for _ in range(new_parents_amount):
                parents_for_next_generation.append(roulette_selection(population))

            for _ in range(CITIES_NUMBER):
                parent1 = random.choice(parents_for_next_generation)
                parent2 = random.choice(parents_for_next_generation)
                child = parent1.create_offspring(parent2)

                # occasional mutation
                mutation_chance = random.random()
                if mutation_chance <= 0.1:
                    child.mutate()

                new_generation.append(copy.deepcopy(child))
        else:
            #  ----------- ELITISM ------------------------
            # Perform Elitism, that mean 10% of fittest population
            # goes to the next generation
            s = int((10 * POPULATION_AMOUNT) / 100)
            new_generation.extend(population[:s])

            # From 50% of fittest population, Individuals will mate to produce offspring
            s = int((90 * POPULATION_AMOUNT) / 100)
            for _ in range(s):
                parent1 = random.choice(population[:250])
                parent2 = random.choice(population[:250])
                child = parent1.create_offspring(parent2)

                # occasional mutation
                mutation_chance = random.random()
                if mutation_chance <= 0.1:
                    child.mutate()

                new_generation.append(copy.deepcopy(child))

        new_generation = sorted(new_generation, key=lambda x: x.fitness, reverse=True)

        if (new_generation[0].fitness > all_time_best_fit) and (new_generation[0].fitness > population[0].fitness):
            all_time_best_fit = new_generation[0].fitness
            convergence_counter = 2500

            print(f"Generation: {generation}\tString: {population[0].chromosomes}\tFitness: {population[0].fitness}")
            # x, y = zip(*population[0].chromosomes)  # Unzip the points into separate x and y arrays
            # # connect first and last point of the graph
            # x = list(x) + [x[0]]
            # y = list(y) + [y[0]]
            # plt.plot(x, y, marker='o', linestyle='solid')
            # plt.xlabel('X')
            # plt.ylabel('Y')
            # plt.title('Traveling Salesman Genetic Algorithm')
            # plt.grid(True)
            # plt.show()
            # plt.pause(0.05)
            population = copy.deepcopy(new_generation)

            # print("new gen is lower")
            # print("next gen fit: ", new_generation[0].fitness)
            # print("current gen fit: ", population[0].fitness)
            # print("all_time BEST: ", all_time_best_fit)
            # print("------------------")
        else:
            convergence_counter -= 1
            # print("new gen is bigger")
            # print("next gen fit: ", new_generation[0].fitness)
            # print("current gen fit: ", population[0].fitness)
            # print("all_time BEST: ", all_time_best_fit)
            # print("------------------")
        generation += 1

    if (new_generation[0].fitness > all_time_best_fit) and (new_generation[0].fitness > population[0].fitness):
        print(f"Generation: {generation}\tString: {population[0].chromosomes}\tFitness: {population[0].fitness}")
        x, y = zip(*population[0].chromosomes)  # Unzip the points into separate x and y arrays
        x = list(x) + [x[0]]
        y = list(y) + [y[0]]
        plt.plot(x, y, marker='o', linestyle='solid')
        plt.xlabel('X-Axis')
        plt.ylabel('Y-Axis')
        plt.title('Traveling Salesman')
        plt.grid(True)
        plt.show()

    #  ---------------------------------------------

if __name__ == '__main__':
    input_array = generate_cities()
    main(input_array)

