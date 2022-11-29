"""
This file contain the common functions to all MetaHeuristics and other will inherit them:

1 - define routes
2 - distance calculate

"""
from dataclasses import dataclass
import random
from copy import deepcopy
import numpy as np

@dataclass
class CommonsVRP():

    def define_routes(self, vetor, demands, vehicle_capacity):
        cap = 0
        vet_aux = list()
        aux = list()
        for i in range(len(vetor)):
            if cap + demands[vetor[i]] <= vehicle_capacity:
                cap += demands[vetor[i]]
                aux.append(vetor[i])
            else:
                vet_aux.append(aux[:])
                aux.clear()
                cap = demands[vetor[i]]
                aux.append(vetor[i])

            if i == (len(vetor) - 1):
                vet_aux.append(aux[:])

        return vet_aux

    def dist_calculate(self, vet_aux, matrix):
        dist = 0
        dist_total = list()
        for rote in vet_aux:
            i = 0
            while i <= len(rote) - 1:
                if i == 0:
                    if len(rote) == 1:
                        dist += matrix[0, (rote[i] - 1)] + matrix[(rote[i] - 1), 0]
                    else:
                        dist += matrix[0, (rote[i] - 1)] + matrix[(rote[i] - 1), (rote[i + 1] - 1)]
                elif i == len(rote) - 1:
                    dist += matrix[(rote[i] - 1), 0]
                else:
                    dist += matrix[(rote[i] - 1), (rote[i + 1] - 1)]
                i += 1
            dist_total.append(dist)
            dist = 0
        return sum(dist_total)

    def change_two_opt(self, solution):
        while True:
            p1 = random.randint(0, len(solution) - 1)
            if p1 == len(solution) - 1:
                continue
            p2 = random.randint(p1, len(solution))
            if p1 == p2:
                continue
            else:
                new_solution = deepcopy(solution)
                new_solution[p1:p2] = np.flipud(solution[p1:p2])
                break
        return np.array(new_solution)