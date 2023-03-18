from reader_tspLIB import ReadTSPLIB
import random
from copy import deepcopy
import numpy as np
#from simulated_annealing import SimulatedAnnealing
from simulated_annealing_with_Instance import SimulatedAnnealing
from dataclasses import dataclass, field
from copy import deepcopy
import commons
import time
import pandas as pd
from instance import Instance

vehicle_capacity = None
n_vehicles = None
matrix = None
demands = None

class Individuo(object):

    def __new__(cls, *args, **kwargs):   #Usado para não relacionar um individuo com outro (substituindo o deepcopy)
        return object.__new__(cls)

    def __init__(self, new_ind= None, size=None, fit=None):
        if new_ind is None:
            self.ind = list(range(size))
            random.shuffle(self.ind)
        else:
            self.ind = new_ind
        if fit is not None:
            self.calculate = fit
        else:
            routes = Instance().compute_vrp_routes(nodes=self.ind, node_demand=demands, capacity=vehicle_capacity)
            self.calculate = Instance().compute_vrp_distance(routes=routes, nodes=self.ind, matrix=matrix)

    def fitness(self):
        return self.calculate


@dataclass
class GeneticAlgorithm():
    path: str
    generations: int = 800
    news: int = 80
    population_size: int = 150
    survivors: int = 120
    base_per_generation: int = field(init=False)

    def __post_init__(self):
        global vehicle_capacity, n_vehicles, matrix, demands

        self.problem = Instance().load_instance(self.path)
        self.nodes = list(range(0, self.problem.dimension))
        vehicle_capacity = self.problem.capacity
        n_vehicles = None
        matrix = self.problem.node_distances
        demands = self.problem.node_demand
        self.base_per_generation = 30
        self.population = list()

    def population_generation(self, pop):
        self.population = [Individuo(size=len(self.nodes)) for i in range(pop)]

    def create_mutation(self):
        new_i = 0
        while new_i < self.news:
            ind = self.population[random.randint(0, self.population_size - 1)].ind.copy()
            n_ind = commons.change_two_opt(ind)
            self.population.append(Individuo(new_ind=n_ind))
            new_i += 1

    def create_mutation_SA(self):
        new_i = 0
        while new_i < self.news:
            SA = SimulatedAnnealing(path=path)
            ind = self.population[random.randint(0, self.population_size - 1)].ind.copy()
            n_ind, _,  fit = SA.simulated_annealing(initial_solution=ind)
            self.population.append(Individuo(new_ind=n_ind))
            new_i += 1

    def sort_population(self):
        self.population = sorted(self.population, key=Individuo.fitness)  #ordenar objetos !!

    def create_new_generation(self):
        self.population.extend([Individuo(size=len(self.nodes)) for i in range(self.population_size - self.survivors)])

    def genetic_algorithm(self):
        break_condition = 250
        break_count = 0
        self.population_generation(self.population_size)
        actual_generation = 0
        last_best = self.population[0].fitness()
        while actual_generation < self.generations:
            self.create_mutation_SA()
            self.sort_population()
            self.population = self.population[:self.survivors]
            self.create_new_generation()
            print(self.population[0].fitness(), actual_generation)
            if last_best == self.population[0].fitness():
                break_count += 1
                if break_count == break_condition:
                    break
            else:
                last_best = self.population[0].fitness()
                break_count = 0
            print(actual_generation)
            actual_generation += 1

        self.sort_population()
        return self.population[0].fitness(), self.population[0].ind



if __name__ == "__main__":
    path = "instances/A-n32-k5.txt"
    GA = GeneticAlgorithm(path=path)
    best, best_value = GA.genetic_algorithm()
    print(best)
    print(best_value)