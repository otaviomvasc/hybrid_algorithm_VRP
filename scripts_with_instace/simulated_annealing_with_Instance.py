
from random import *
import tsplib95
import numpy as np
from dataclasses import dataclass
import copy
import random
import math
from reader_tspLIB import ReadTSPLIB
import commons
from instance import Instance

@dataclass
class SimulatedAnnealing():
    path: str
    T: float = 500
    alfa: float = 0.05
    max_times: int = 400

    def __post_init__(self):
        self.problem = Instance().load_instance(self.path)
        self.nodes = list(range(0, self.problem.dimension))
        self.vehicle_capacity = self.problem.capacity
        self.n_vehicles = None
        self.matrix = self.problem.node_distances
        self.demands = self.problem.node_demand
        self.initial_vector = copy.deepcopy(self.nodes[1:]) #TODO: Change this use the first node

    def randon_change(self, vetor):
        #TODO: Use 2-opt to create new vector? PLEASE USE NUMPY TO IMPROVE THIS!!!!
        pos_change_1 = (randrange(0, len(vetor)))
        node1 = vetor[pos_change_1]
        pos_change_2 = (randrange(0, len(vetor)))
        node2 = vetor[pos_change_2]
        vetor[pos_change_1] = node2
        vetor[pos_change_2] = node1


        return vetor

    def energy_calculate(self, new_vetor, initial=False):
        new_vetor = new_vetor if initial else commons.change_two_opt(new_vetor)
        separte_routes = Instance().compute_vrp_routes(nodes = new_vetor, node_demand=self.demands, capacity=self.vehicle_capacity)
        dist_total = Instance().compute_vrp_distance(routes=separte_routes, nodes=new_vetor, matrix=self.matrix)

        return new_vetor, dist_total

    def reduct_t_geometric(self, T):
        return T * self.alfa

    def generate_initial_solution(self):
        a=0

    def simulated_annealing(self, initial_solution=None):
        if initial_solution is not None:
            vetor = copy.deepcopy(initial_solution)
        else:
            vetor = copy.deepcopy(self.nodes[1:])
        _, e_base = self.energy_calculate(vetor, True)
        times = 0
        T = self.T
        vector = vetor
        while times < self.max_times:
            vector_change, e_2 = self.energy_calculate(vetor, False)
            delta = e_2 - e_base
            if delta < 0:
                vector = vector_change[:]
                e_base = e_2
            else:
                x = random.random()
                if x < (math.exp(-delta / T)):
                    vector = vector_change[:]
                    e_base = e_2
            times += 1
            T = self.reduct_t_geometric(T)
            if T < 1e-6:
                break
        #best_rote = commons.define_routes(vector or vetor, self.demands, self.vehicle_capacity)

        #best_rote = self.define_routes(vector)
        return vector, e_base #best_rote,

    def multiple_executions(self, number_executions=500, initial_solution=None):
        cont = 0
        list_result = list()
        while cont <= number_executions:
            _, result = self.simulated_annealing(initial_solution)
            cont += 1
            list_result.append(result)

        return list_result, min(list_result) #TODO: return the best rote

if __name__ == '__main__':
    pass
