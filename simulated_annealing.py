
from random import *
import tsplib95
import numpy as np
from dataclasses import dataclass
import copy
import random
import math
from reader_tspLIB import ReadTSPLIB
import commons
import pandas as pd

@dataclass
class SimulatedAnnealing():
    path: str
    T: float = 1000
    alfa: float = 0.1
    max_times: int = 1000

    def __post_init__(self):
        self.problem = ReadTSPLIB(self.path)
        self.nodes = self.problem.get_node_list()
        self.nodes = self.problem.get_node_list()
        self.vehicle_capacity = self.problem.get_vehicle_capacites()
        self.n_vehicles = self.problem.get_number_of_vehicles()
        self.matrix = self.problem.get_matrix()
        self.demands = self.problem.get_demands()
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
        separte_routes = commons.define_routes(new_vetor, self.demands, self.vehicle_capacity)
        dist_total = commons.dist_calculate(separte_routes, self.matrix)

        return new_vetor, dist_total

    def reduct_t_geometric(self, T):
        return T * self.alfa

    def generate_initial_solution(self):
        a=0

    def simulated_annealing(self, initial_solution=None):
        if initial_solution is not None:
            vector = copy.deepcopy(initial_solution)
        else:
            vector = copy.deepcopy(self.nodes[1:])
        _, e_base = self.energy_calculate(vector, True)
        times = 0
        T = self.T
        while times < self.max_times:
            vector_change, e_2 = self.energy_calculate(vector, False)
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
        return vector, _, e_base

    def multiple_executions(self, number_executions=500, initial_solution=None):
        cont = 0
        list_result = list()
        while cont <= number_executions:
            _, result = self.simulated_annealing(initial_solution)
            cont += 1
            list_result.append(result)

        return list_result, min(list_result) #TODO: return the best rote

if __name__ == '__main__':
    path = "instances/A-n33-k6.txt"
    SA=SimulatedAnnealing(path=path)
    _, _, v = SA.simulated_annealing()
    print(v)
    # same_repetitions = 30
    # save_data = 10
    # T_ = np.arange(1000, 20001, 1000)
    # alfa_ = np.arange(0.01, 0.999, 0.1)
    # rep = 0
    # all_data = list()
    # result_aux = list()
    # cont_save_data = 0
    # for t in T_:
    #     for alfa in alfa_:
    #         print(t, alfa)
    #         while rep < same_repetitions:
    #             SA = SimulatedAnnealing(path=path, T=t, alfa=alfa)
    #             _, _, v = SA.simulated_annealing()
    #             result_aux.append(v)
    #             rep += 1
    #
    #         result = {'T': t, 'alfa': alfa, "best_value": result_aux[:]}
    #         all_data.append(result)
    #         cont_save_data += 1
    #         rep = 0
    #         result_aux.clear()
    #
    #     if cont_save_data == save_data:
    #         df = pd.DataFrame(all_data)
    #         with pd.ExcelWriter('dados_SA.xlsx', engine="openpyxl", mode='a', if_sheet_exists="replace") as writer:
    #             df.to_excel(writer, 'Planilha')
    #         cont_save_data = 0