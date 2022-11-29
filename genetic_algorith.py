from reader_tspLIB import ReadTSPLIB
import random
from copy import deepcopy
import numpy as np
from simulated_annealing import SimulatedAnnealing
from dataclasses import dataclass, field
from copy import deepcopy
from commons import CommonsVRP


@dataclass
class GeneticAlgorithm(CommonsVRP):
    path: str
    generations: int = 2000
    news: int = 20
    population_size: int = 100
    survivors: int = 50
    base_per_generation: int = field(init=False)

    def __post_init__(self):  #TODO: Is necessary the same post_init of simulated annealing ou i can get thw two?
        self.problem = ReadTSPLIB(self.path)
        self.nodes = self.problem.get_node_list()
        self.vehicle_capacity = self.problem.get_vehicle_capacites()
        self.n_vehicles = self.problem.get_number_of_vehicles()
        self.matrix = self.problem.get_matrix()
        self.demands = self.problem.get_demands()
        self.initial_vector = deepcopy(self.nodes[1:])
        self.commons = CommonsVRP()
        self.base_per_generation = 10


    def population_generation(self, nodes, pop):
        population = list()
        individuo = list()
        i = 0
        nodes_aux = deepcopy(nodes)
        while i < pop:
            while True:
                if len(nodes_aux) == 0:
                    break
                p = random.randint(0, len(nodes_aux) - 1)
                individuo.append(nodes_aux[p])
                nodes_aux = np.delete(nodes_aux, p, 0)
            population.append(individuo[:])
            individuo.clear()
            nodes_aux = deepcopy(nodes)
            i += 1
        return np.array(population)

    def fitness_calculation(self, population: list()):
        fitness = list()
        for ind in population:
            routes = self.commons.define_routes(ind, self.demands, self.vehicle_capacity)
            dist = self.commons.dist_calculate(routes, self.matrix)
            fitness.append(dist)
        return np.array(fitness)

    def create_mutation(self, population, fitness):
        new_i = 0
        while new_i < self.news:
            ind = population[random.randint(0, self.population_size - 1)]
            n_ind = self.commons.change_two_opt(ind)
            n_fitness = self.fitness_calculation([n_ind])
            fitness = np.insert(fitness, 0, n_fitness, axis=0)
            population = np.insert(population, 0, n_ind, axis=0)
            new_i += 1

        return population, fitness

    def sort_population(self, population, fitness):
        indices = list(range(len(fitness)))
        indices.sort(key=lambda i: fitness[i])
        population = np.array([population[i] for i in indices])
        fitness = np.array([fitness[i] for i in indices])

        return population, fitness

    def create_new_generation(self, population, fitness):
        i = 0
        while i < (self.population_size - self.survivors):
            ind_base = population[random.randint(0, self.survivors - 1)]
            new_pop = self.population_generation(ind_base, self.base_per_generation)
            new_fitness = self.fitness_calculation(new_pop)
            fitness = np.concatenate((fitness, new_fitness), axis=0)
            population = np.concatenate((population, new_pop), axis=0)
            i += self.base_per_generation

        return population, fitness

    def genetic_algorithm(self, save=False):
        data = list()
        population = self.population_generation(self.initial_vector, self.population_size)
        fitness = self.fitness_calculation(population)
        actual_generation = 0

        while actual_generation < self.generations:
            #print(actual_generation)
            population, fitness = self.create_mutation(population, fitness)
            population, fitness = self.sort_population(population, fitness)

            # Elitismo - Retirar uma quantidade de novos cidadões
            #TODO: Is it necessary New method? Is There better way to connect population and fitness? Dict maybe?
            population = population[:int(self.survivors)]
            fitness = fitness[:int(self.survivors)]

            population, fitness = self.create_new_generation(population, fitness)

            actual_generation += 1


        population, fitness = self.sort_population(population, fitness)
        if not save:
            return population, fitness, np.insert(population[0], 0, 1, axis=0), fitness[0]
        else:
            return fitness[0]

if __name__ == '__main__':
    path = "instances/eilb101.vrp.txt"
