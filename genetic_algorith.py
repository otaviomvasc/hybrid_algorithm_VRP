from reader_tspLIB import ReadTSPLIB
import random
from copy import deepcopy
import numpy as np
from simulated_annealing import SimulatedAnnealing
from dataclasses import dataclass, field
from copy import deepcopy
from commons import CommonsVRP
import time

@dataclass
class GeneticAlgorithm(CommonsVRP):
    path: str
    generations: int = 2000
    news: int = 20
    population_size: int = 100
    survivors: int = 50
    base_per_generation: int = field(init=False)

    def __post_init__(self):
        self.problem = ReadTSPLIB(self.path)
        self.nodes = self.problem.get_node_list()
        self.vehicle_capacity = self.problem.get_vehicle_capacites()
        self.n_vehicles = self.problem.get_number_of_vehicles()
        self.matrix = self.problem.get_matrix()
        self.demands = self.problem.get_demands()
        self.initial_vector = deepcopy(self.nodes[1:])
        self.commons = CommonsVRP()
        self.base_per_generation = 30


    def population_generation(self, nodes, pop):
        start = time.time()
        population = list()
        i = 0
        nodes_aux = deepcopy(nodes)
        while i < pop:
            random.shuffle(nodes_aux)
            n = deepcopy(nodes_aux)
            population.append(n)
            i += 1
        end = time.time()
        print("geração da população :", end - start)
        return np.array(population)

    def fitness_calculation(self, population: list()):
        start = time.time()
        fitness = list()
        for ind in population:
            routes = self.commons.define_routes(ind, self.demands, self.vehicle_capacity)
            dist = self.commons.dist_calculate(routes, self.matrix)
            fitness.append(dist)
        end = time.time()
        print("calculo do fitness levou :", end - start)
        return np.array(fitness)

    def create_mutation(self, population):
        start = time.time()
        new_i = 0
        while new_i < self.news:
            ind = population[random.randint(0, self.population_size - 1)]
            n_ind = self.commons.change_two_opt(ind)
            population = np.insert(population, 0, n_ind, axis=0)
            new_i += 1
        end = time.time()
        print("criação da mutação :", end - start)
        return population

    def sort_population(self, population, fitness):
        start = time.time()
        indices = list(range(len(fitness)))
        indices.sort(key=lambda i: fitness[i])
        population = np.array([population[i] for i in indices])
        fitness = np.array([fitness[i] for i in indices])
        end = time.time()
        print("sort_population :", end - start)
        return population, fitness

    def create_new_generation(self, population):
        start = time.time()
        recovery = self.population_size - self.survivors
        ind_base = population[random.randint(0, self.survivors - 1)]
        new_pop = self.population_generation(ind_base, recovery)
        population = np.concatenate((population, new_pop), axis=0)
        end = time.time()
        print("Criar nova geração :", end - start)
        return population

    def genetic_algorithm(self, save=False):
        data = list()
        population = self.population_generation(self.initial_vector, self.population_size)
        actual_generation = 0
        while actual_generation < self.generations:

            start = time.time()
            population = self.create_mutation(population)
            fitness = self.fitness_calculation(population)
            population, fitness = self.sort_population(population, fitness)
            # Elitismo - Retirar uma quantidade de novos cidadões
            #TODO: Is it necessary New method? Is There better way to connect population and fitness? Dict maybe?
            population = population[:int(self.survivors)]
            population = self.create_new_generation(population)
            end = time.time()
            print(f"tempo de execução da geração {actual_generation} :, {end - start}")

            actual_generation += 1

        fitness = self.fitness_calculation(population)
        population, fitness = self.sort_population(population, fitness)

        if not save:
            return population, fitness, np.insert(population[0], 0, 1, axis=0), fitness[0]
        else:
            return fitness[0]

if __name__ == '__main__':
    path = "instances/eilb101.vrp.txt"
