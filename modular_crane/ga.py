import math
import openpyxl
import random


class Chromosome:
    def __init__(self, list_crane, list_trailer, list_unit, list_grid, index_crane, index_trailer, index_unit):
        self.list_crane = list_crane
        self.list_trailer = list_trailer
        self.list_unit = list_unit
        self.list_grid = list_grid
        self.index_crane = index_crane
        self.index_trailer = index_trailer
        self.index_unit = index_unit

    def zero_chromosome(self):
        # get grid list(x,y) and make zero chromosome list(0,0,0...)
        zero_chromosome_crane = []
        zero_chromosome_trailer = []

        for i in range(self.index_trailer):
            zero_chromosome_crane.append(0)
        for i in range(self.index_trailer, self.index_unit):
            zero_chromosome_trailer.append(0)

        zero_chromosome = zero_chromosome_crane + zero_chromosome_trailer

        return zero_chromosome, zero_chromosome_crane, zero_chromosome_trailer

    def random_chromosome(self):
        # from zero chromosome make random chromosome list(1,0,0,1...)
        zero_chromosome, zero_chromosome_crane, zero_chromosome_trailer = self.zero_chromosome()

        a = random.randrange(self.index_trailer)
        b = random.randrange(self.index_trailer, self.index_unit)

        zero_chromosome[a] = 1
        zero_chromosome[b] = 1
        random_chromosome = zero_chromosome
        return random_chromosome

    def get_location(self, random_chromosome):
        # from random chromosome get location (x,y)
        index_list = [i for i, value in enumerate(random_chromosome) if value == 1]
        index_x = index_list[0]
        index_y = index_list[1]

        location_crane = self.list_grid[index_x]
        location_trailer = self.list_grid[index_y]
        location_unit = self.list_grid[self.index_unit:]

        return location_crane, location_trailer, location_unit

    def get_distance(self, location1, location2):
        distance_x = location1[0] - location2[0]
        distance_y = location1[1] - location2[1]
        distance = math.sqrt((distance_x**2 + distance_y**2))

        return distance

    def get_max_distance(self, random_chromosome):
        location_crane, location_trailer, location_unit = self.get_location(random_chromosome)
        list_distance = []

        list_distance.append(self.get_distance(location_crane, location_trailer))
        for i in location_unit:
            list_distance.append(self.get_distance(location_crane, i))

        max_distance = max(list_distance)
        return max_distance


class GeneticAlgorithm(Chromosome):

    def parameters(self, number_generation, size_population, rate_crossover, rate_mutation):
        self.number_generation = number_generation
        self.size_population = size_population
        self.rate_crossover = rate_crossover
        self.rate_mutation = rate_mutation

    def generate_initial_population(self):
        list_population = []
        self.chromosome = Chromosome(self.list_crane, self.list_trailer, self.list_unit, self.list_grid,
                                     self.index_crane, self.index_trailer, self.index_unit)

        while len(list_population) < self.size_population:
            random_chromosome = self.chromosome.random_chromosome()
            if random_chromosome in list_population:
                pass
            else:
                list_population.append(random_chromosome)

        return list_population

    def fit(self, list_population):
        list_fitness = []
        list_chromosome = []
        for i in list_population:
            list_chromosome.append(i)
            fitness = self.chromosome.get_max_distance(i)
            list_fitness.append(fitness)

        list = zip(list_fitness, list_chromosome)
        new_list = sorted(list, key=lambda t: t[0]) #작은게 앞에

        sorted_list_population = [p for f, p in new_list]
        sorted_list_fitness = [f for f, p in new_list]

        return sorted_list_population, sorted_list_fitness

    def fitness(self, list_population):
        sorted_list_population, sorted_list_fitness = self.fit(list_population)

        return sorted_list_population

    def evaluate(self, list_population):
        sorted_list_population, sorted_list_fitness = self.fit(list_population)
        location_crane, location_trailer, location_unit = self.get_location(sorted_list_population[0]
                                                                            )
        print('Minimum distance is : %d' %sorted_list_fitness[0])
        print('Location of the crane is :', location_crane)
        print('Location of the trailer is :', location_trailer)

    def test(self, list_population):
        list = self.fitness(list_population)
        for i in list:
            print(self.get_location(i))

    def selection(self, list_population):
        sorted_list_population, sorted_list_fitness = self.fit(list_population)

        total_fitness = (sum(sorted_list_fitness))
        relative_fitness = [f / total_fitness for f in sorted_list_fitness]
        probabilities = [sum(relative_fitness[:i + 1]) for i in range(len(relative_fitness))]

        parent_population = []
        for n in range(2):
            r = random.random()
            for (i, individual) in enumerate(sorted_list_population):
                if r <= probabilities[i]:
                    parent_population.append(list(individual))
                    break

        return parent_population

    def crossover(self, parent_population):
        chromosome1 = parent_population[0]
        chromosome2 = parent_population[1]

        crane_chromosome1 = chromosome1[:self.index_trailer]
        crane_chromosome2 = chromosome2[:self.index_trailer]
        trailer_chromosome1 = chromosome1[self.index_trailer:]
        trailer_chromosome2 = chromosome2[self.index_trailer:]

        crane_child_chromosome = []
        trailer_child_chromosome = []
        for i, v in enumerate(crane_chromosome1):
            if random.random() < self.rate_crossover:
                crane_child_chromosome.append(v)
            else:
                crane_child_chromosome.append(crane_chromosome2[i])

        for i, v in enumerate(trailer_chromosome1):
            if random.random() < self.rate_crossover:
                trailer_child_chromosome.append(v)
            else:
                trailer_child_chromosome.append(trailer_chromosome2[i])

        if crane_child_chromosome.count(1) > 1:
            index = []
            for i, v in enumerate(crane_child_chromosome):
                if v == 1:
                    index.append(i)
            crane_child_chromosome[random.choice(index)] = 0
        elif crane_child_chromosome.count(1) == 0:
            i = random.randrange(self.index_trailer)
            crane_child_chromosome[i] = 1

        if trailer_child_chromosome.count(1) > 1:
            index = []
            for i, v in enumerate(trailer_child_chromosome):
                if v == 1:
                    index.append(i)
            trailer_child_chromosome[random.choice(index)] = 0
        elif trailer_child_chromosome.count(1) == 0:
            i = random.randrange(self.index_unit - self.index_trailer)
            trailer_child_chromosome[i] = 1

        child_chromosome = crane_child_chromosome + trailer_child_chromosome

        return child_chromosome

    def mutation(self, child_chromosome):
        child_crane_chromosome = child_chromosome[:self.index_trailer]
        index_crane = child_crane_chromosome.index(1)
        child_trailer_chromosome = child_chromosome[self.index_trailer:]
        index_trailer = child_trailer_chromosome.index(1)

        if random.random() < self.rate_mutation:
            index1 = random.randrange(len(child_crane_chromosome))
            number1 = child_crane_chromosome[index1]
            child_crane_chromosome[index_crane] = number1
            child_crane_chromosome[index1] = 1

            index2 = random.randrange(len(child_trailer_chromosome))
            number2 = child_trailer_chromosome[index2]
            child_trailer_chromosome[index_trailer] = number2
            child_trailer_chromosome[index2] = 1

        new_chromosome = child_crane_chromosome + child_trailer_chromosome

        return new_chromosome

    def evolve(self, list_population):
        child_population = []
        while len(child_population) < self.size_population:
            parent_population = self.selection(list_population)
            child_chromosome = self.crossover(parent_population)
            new_chromosome = self.mutation(child_chromosome)
            if new_chromosome in child_population:
                pass
            else:
                child_population.append(new_chromosome)

        return child_population

    def GA(self):
        initial_population = self.generate_initial_population()
        for i in range(self.number_generation):
            print(i+1, '/ %d' %self.number_generation)
            self.evaluate(initial_population)
            next_population = self.evolve(initial_population)
            initial_population = next_population

        return initial_population