from reader_tspLIB import ReadTSPLIB
import random
from copy import deepcopy
import numpy as np
from simulated_annealing import SimulatedAnnealing
from dataclasses import dataclass, field
from copy import deepcopy
import commons
import time
from instance import Instance

vehicle_capacity = None
n_vehicles = None
matrix = None
demands = None

class Individuo(object):

    def __new__(cls, *args, **kwargs):   #Usado para não relacionar um individuo com outro (substituindo o deepcopy)
        return object.__new__(cls)

    def __init__(self, new_ind = None, size = None):
        if new_ind is None:
            self.ind = list(range(1, size))
            random.shuffle(self.ind)
        else:
            self.ind = new_ind
        routes = commons.define_routes(vetor=self.ind, demands=demands, vehicle_capacity=vehicle_capacity)
        self.calculate = commons.dist_calculate(vet_aux=routes, matrix=matrix)

    def fitness(self):
        return self.calculate


@dataclass
class GeneticAlgorithm():
    path: str
    generations: int = 2000
    news: int = 20
    population_size: int = 100
    survivors: int = 50
    base_per_generation: int = field(init=False)

    def __post_init__(self):
        global vehicle_capacity, n_vehicles, matrix, demands

        self.problem = ReadTSPLIB(self.path)
        self.nodes = self.problem.get_node_list()
        vehicle_capacity = self.problem.get_vehicle_capacites()
        n_vehicles = self.problem.get_number_of_vehicles()
        matrix = self.problem.get_matrix()
        demands = self.problem.get_demands()
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

    def sort_population(self):
        self.population = sorted(self.population, key=Individuo.fitness)  #ordenar objetos !!

    def create_new_generation(self):
        self.population.extend([Individuo(size=len(self.nodes)) for i in range(self.population_size - self.survivors)])


    def genetic_algorithm(self):
        self.population_generation(self.population_size)
        actual_generation = 0
        while actual_generation < self.generations:


            self.create_mutation()
            self.sort_population()
            self.population = self.population[:self.survivors]
            self.create_new_generation()
            #   print(self.population[0].fitness(), actual_generation)
            actual_generation += 1

        self.sort_population()
        return self.population[0].fitness(), self.population[0].ind



