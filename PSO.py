import random
from copy import deepcopy

import commons
import numpy as np
from reader_tspLIB import ReadTSPLIB
import random

class Individuo(object):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, new_ind=None, size=None, change_vel=None):
        if new_ind is None:
            ind = list(range(1, size))
            position = [random.uniform(-1,1) for i in range(1,size)]
            self.order_per_position(ind, position)
            self.velocity = np.array([random.uniform(-4.0,4.0) for i in range(len(self.ind))])
            routes = commons.define_routes(vetor=self.ind, demands=demands, vehicle_capacity=vehicle_capacity)
            self.fit = commons.dist_calculate(vet_aux=routes, matrix=matrix)
            self.best_local = deepcopy(self)


    def best_local_actualize(self):
        if self.fitness() < self.best_local.fitness():
            self.best_local = deepcopy(self)

    def fitness_calculation(self, demands, vehicle_capacity, matrix):
        routes = commons.define_routes(vetor=self.ind, demands=demands, vehicle_capacity=vehicle_capacity)
        self.fit = commons.dist_calculate(vet_aux=routes, matrix=matrix)

    def order_per_position(self, ind=None, position=None):
        if ind is not None and position is not None:
            indices = list(range(len(ind)))
            indices.sort(key=lambda i: position[i])
            self.ind = [ind[i] for i in indices]
            self.position = np.array([position[i] for i in indices])
        else:
            indices = list(range(len(self.ind)))
            indices.sort(key=lambda i: self.position[i])
            self.position = np.array([self.position[i] for i in indices])
            self.ind = [self.ind[i] for i in indices]

    def fitness(self):
        return self.fit

    def velocity_calculation(self, best, c1r1, c2r2):
        self.velocity = self.velocity + c1r1 * (self.best_local.position - self.position) + c2r2 * (best.position - self.position)


if __name__ == "__main__":
    path = "instances/eil23.vrp.txt"

    problem = ReadTSPLIB(path=path)
    vehicle_capacity = problem.get_vehicle_capacites()
    n_vehicles = problem.get_number_of_vehicles()
    matrix = problem.get_matrix()
    demands = problem.get_demands()
    coords = problem.get_coords()
    nodes = problem.get_node_list()
    pop = 500
    iterations = 400
    i = 0
    c1r1 = 1.2
    c2r2 = 1.8


    population = [Individuo(size=len(nodes)) for i in range(pop)]
    g_best = min([p.fitness() for p in population])
    best = [p for p in population if p.fitness() == g_best][0]

    while i < iterations:
        #atualizar o position, fit e best_local
        for ind in population:
            ind.velocity_calculation(best, c1r1, c2r2)
            ind.position = ind.position + ind.velocity
            ind.order_per_position()
            ind.fitness_calculation(demands, vehicle_capacity, matrix)
            ind.best_local_actualize()


        g_best_candidate = min([p.fitness() for p in population])
        best_candidate = [p for p in population if p.fitness() == g_best_candidate][0]
        if best_candidate.fitness() < best.fitness():
            best = deepcopy(best_candidate)
        print(f'iteração {i} gerou um fitness de: {best.fitness()}')
        i += 1
    print(f'Melhor best foi de: {best.fitness()}')