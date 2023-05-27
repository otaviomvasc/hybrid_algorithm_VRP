from reader_tspLIB import ReadTSPLIB
import random
from copy import deepcopy
import numpy as np
from simulated_annealing import SimulatedAnnealing
from dataclasses import dataclass, field
from copy import deepcopy
import commons
import time
import pandas as pd

vehicle_capacity = None
n_vehicles = None
matrix = None
demands = None

class Individuo(object):

    def __new__(cls, *args, **kwargs):   #Usado para não relacionar um individuo com outro (substituindo o deepcopy)
        return object.__new__(cls)

    def __init__(self, new_ind= None, size=None, fit=None):
        if new_ind is None:
            self.ind = list(range(2, size + 1))
            random.shuffle(self.ind)
        else:
            self.ind = new_ind
        if fit is not None:
            self.calculate = fit
        else:
            routes = commons.define_routes(vetor=self.ind, demands=demands, vehicle_capacity=vehicle_capacity)
            self.calculate = commons.dist_calculate(vet_aux=routes, matrix=matrix)

    def fitness(self):
        return self.calculate


@dataclass
class Hibryd_Genetic_Algorithm():
    path: str
    T_SA: int = 10000
    alfa_SA: float = 0.1
    generations: int = 1400
    news: int = 350
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
        self.SA = SimulatedAnnealing(path=self.path, T=self.T_SA, alfa=self.alfa_SA)
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
        # if self.T_SA and self.alfa_SA:
        #     SA = SimulatedAnnealing(path=self.path, T=self.T_SA, alfa=self.alfa_SA)
        # else:
        #     SA = SimulatedAnnealing(path=path)
        ind = self.population[0].ind.copy()
        n_ind, _,  fit = self.SA.simulated_annealing(initial_solution=ind)
        self.population.append(Individuo(new_ind=n_ind))

    def sort_population(self):
        self.population = sorted(self.population, key=Individuo.fitness)  #ordenar objetos !!

    def create_new_generation(self):
        self.population.extend([Individuo(size=len(self.nodes)) for i in range(self.population_size - self.survivors)])

    def specialist(self):
        nodes = list(self.nodes[1:])
        cur_node = random.randint(2, len(self.nodes))
        solution = [cur_node]
        free_nodes = set(nodes)
        free_nodes.remove(cur_node)
        while free_nodes:
            next_node = min(free_nodes, key=lambda x: matrix[cur_node, x])
            free_nodes.remove(next_node)
            solution.append(next_node)
            cur_node = next_node

        self.population.append(Individuo(new_ind=solution))

    def genetic_algorithm(self):

        self.population_generation(self.population_size)
        break_condition = 300
        break_count = 0
        actual_generation = 0
        if len(self.nodes) > 50:
            self.specialist()
        best = self.population[0].fitness()
        while actual_generation < self.generations:
            self.create_mutation_SA()
            self.create_mutation()
            self.sort_population()
            if best == self.population[0].fitness():
                break_count += 1
                if break_count == break_condition:
                    break
            else:
                break_count = 0
                best = self.population[0].fitness()
            #print(self.population[0].fitness(), actual_generation)
            self.create_mutation_SA()
            self.population = self.population[:self.survivors]
            self.create_new_generation()
            #print(actual_generation)
            actual_generation += 1

        self.sort_population()
        return self.population[0].fitness(), self.population[0].ind



if __name__ == "__main__":
    inicio = time.time()
    path = "instances/A-n32-k5.txt"
    GA = Hibryd_Genetic_Algorithm(path=path)
    best, best_value = GA.genetic_algorithm()
    fim = time.time()
    print(best)
    print(best_value)
    print(fim - inicio)


    #Rodar só o SA partindo de uma instância com valor 850 30000x e ver como se comporta
    #com a variação aleatória dos parametros