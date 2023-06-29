"""
A genetic algorithm for maximizing a bitstring.

The integer is encoded as a bitstring (list of 0s or 1s). Fitness is calculated with either the value of the bitstring
or the number of 1s in the bitstring (both are included for a comparison). Crossover is a single point crossover and
mutation is a bit flip mutation.
"""
from random import choices, random, randrange

import matplotlib.pyplot as plt

from src.crossover import one_point_crossover
from src.mutation import bit_flip_mutation
from src.selection import tournament_selection

BIT_STRING_LENGTH = 16
POPULATION_SIZE = 10
GENERATIONS = 100
CROSSOVER_RATE = 0.70
MUTATION_RATE = 0.10


def value_fitness(chromosome: list) -> int:
    """
    Calculate the decimal value of the chromosome (bitstring).

    :param chromosome: Chromosome (bitstring) to evaluate
    :return: The decimal value of the chromosome (bitstring)
    """
    return int("".join(str(bit) for bit in chromosome), 2)


def ones_fitness(chromosome: list) -> int:
    """
    Count the number of 1s (ones) in the chromosome (bitstring).

    :param chromosome: Chromosome (bitstring) to evaluate
    :return: The number of 1s (ones) in the chromosome (bitstring).
    """
    number_of_ones = 0
    for bit in chromosome:
        number_of_ones += bit
    return number_of_ones


def run_max_bitstring_ga():
    # Bookkeeping
    generation_max_fitness = []
    generation_average_fitness = []

    # Initialize
    population = []
    population_fitness = []
    for _ in range(POPULATION_SIZE):
        chromosome = choices([0, 1], k=BIT_STRING_LENGTH)
        population.append(chromosome)

    # Run for a Specified Number of Generations (Termination)
    for generation in range(GENERATIONS):
        # Evaluate
        population_fitness = []
        for chromosome in population:
            fitness = value_fitness(chromosome)
            population_fitness.append(fitness)

        # Bookkeeping
        generation_max_fitness.append(max(population_fitness))
        generation_average_fitness.append(sum(population_fitness) // len(population_fitness))

        # Selection
        mating_pool = []
        for _ in range(POPULATION_SIZE):
            tournament_indices = choices(range(POPULATION_SIZE), k=2)
            chromosome = tournament_selection(population, population_fitness, tournament_indices)
            mating_pool.append(chromosome)

        # Variation (Crossover)
        for i in range(0, POPULATION_SIZE, 2):
            if random() < CROSSOVER_RATE:
                crossover_point = randrange(BIT_STRING_LENGTH)
                chromosome_1, chromosome_2 = one_point_crossover(mating_pool[i], mating_pool[i + 1], crossover_point)
                mating_pool[i] = chromosome_1
                mating_pool[i + 1] = chromosome_2

        # Variation (Mutation)
        for i in range(POPULATION_SIZE):
            if random() < MUTATION_RATE:
                mutation_point = randrange(BIT_STRING_LENGTH)
                chromosome = bit_flip_mutation(mating_pool[i], mutation_point)
                mating_pool[i] = chromosome

        population = mating_pool

    population_fitness = []
    for chromosome in population:
        fitness = value_fitness(chromosome)
        population_fitness.append(fitness)
    print(population_fitness)
    print(population)
    generation_max_fitness.append(max(population_fitness))
    generation_average_fitness.append(sum(population_fitness) // len(population_fitness))

    # plt.plot(generation_max_fitness)
    # plt.plot(generation_average_fitness)
    # plt.show()


if __name__ == "__main__":
    run_max_bitstring_ga()