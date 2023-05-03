import random
from copy import deepcopy

import commons
import numpy as np
from reader_tspLIB import ReadTSPLIB
import random
from dataclasses import dataclass, field


"""
1 - Criar uma classe de população de membros
2 - Criar uma classe de individuos
    cada individuo de acordo com o número de nós
    criar a posição aleatória para cada individuo
    ordenar a lista de posição e a lista de individuos de acordo com a posição
        Dessa forma cada nó tem uma posição : [0,3,4,7,8] -> [-0.23, -0.12, 0, 2, 2.2]
    criar vetor de velocidades aleatórias
    criar melhor local - Individuo()
    
3 - Método para calcular fitness() - Individuo
4 - melhor global (parcial) - Na classe população
5 - melhor global (geral) - Na classe população
6 - calcular velocidade - Individuo
7 - calcular posição - Individuo

"""
vehicle_capacity = None
n_vehicles = None
matrix = None
demands = None

@dataclass
class PSO():
    path: str
    iterations: int = 100
    c1: float = 0.8
    c2: float = 0.8
    ind: int = 100
    w: float = 0.6
    pop_size: int = 100
    neighbors: int = 10

    def __post_init__(self):
        global vehicle_capacity, n_vehicles, matrix, demands

        self.problem = ReadTSPLIB(self.path)
        self.nodes = self.problem.get_node_list()[1:]
        vehicle_capacity = self.problem.get_vehicle_capacites()
        n_vehicles = self.problem.get_number_of_vehicles()
        matrix = self.problem.get_matrix()
        demands = self.problem.get_demands()
        self.population = list()

    def create_population(self):
        self.population = [Individuo(size=len(self.nodes)) for _ in range(self.pop_size)]

    def velocity_calculate(self):
        r1 = random.random()
        r2 = random.random()
        for ind in self.population:
            ind.velocity = self.w * ind.velocity + (self.c1 * r1 * (ind.best_local['pos'] - ind.position)) \
                           + (self.c2 * r2 * (ind.best_global['pos'] - ind.position))

    def position_calculate(self):
        for ind in self.population:
            ind.position += ind.velocity

    def fitness_calculate(self):
        for ind in self.population:
            ind.order_ind()
            ind.fitness_calculate()

    def best_local_actualize(self):
        for ind in self.population:
            if ind.fit < ind.best_local['fit']:
                ind.best_local = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}

    def best_global_actualize(self):
        """
        :posicao 0 da população vai verificar do 0 até 0 19 e usar de global o de menor valor
        posicao 1 vai olhar do 1 até 0 20
        posicao 45 vai olhar o?
        usar lógica básica pra fazer o anel, mas depois trocar pra modulo
        """
        i = 0
        while i < self.pop_size:
            if i - self.neighbors < 0:
                best_fit = self.population[i].best_global['fit'] if self.population[i].best_global is not None else self.population[i].fit
                best_ind = self.population[i].best_global
                start = self.pop_size + (i - self.neighbors)
                mid = 0
                end = i + self.neighbors

                for ind in self.population[start:]:
                    if ind.best_local['fit'] < best_fit:
                        best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
                        best_fit = best_ind['fit']

                for ind in self.population[mid:end + 1]:
                    if ind.best_local['fit'] < best_fit:
                        best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
                        best_fit = best_ind['fit']

                for ind in self.population[start:]:
                    ind.best_global = best_ind

                for ind in self.population[mid: end + 1]:
                    ind.best_global = best_ind
                i += 1
                print(i)

            elif self.pop_size - i < self.neighbors:
                start = i - self.neighbors
                mid = 0
                end = self.neighbors - (self.pop_size - 1)
                for ind in self.population[start:mid + 1]:
                    if ind.best_local['fit'] < best_fit:
                        best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
                        best_fit = best_ind['fit']

                for ind in self.population[mid: end + 1]:
                    if ind.best_local['fit'] < best_fit:
                        best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
                        best_fit = best_ind['fit']

                for ind in self.population[start:mid + 1]:
                    ind.best_global = best_ind

                for ind in self.population[mid: end + 1]:
                    ind.best_global = best_ind
                i += 1
                print(i)

            else:
                start = i - self.neighbors
                mid = i
                end = i + self.neighbors

                for ind in self.population[start:mid + 1]:
                    if ind.best_local['fit'] < best_fit:
                        best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
                        best_fit = best_ind['fit']

                for ind in self.population[mid: end + 1]:
                    if ind.best_local['fit'] < best_fit:
                        best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
                        best_fit = best_ind['fit']

                for ind in self.population[start:mid + 1]:
                    ind.best_global = best_ind

                for ind in self.population[mid: end + 1]:
                    ind.best_global = best_ind
                i += 1
                print(i)


# @dataclass
# class PSO_Instance():
#     path: str
#     iterations: int = 100
#     c1: float = 0.8
#     c2: float = 0.8
#     ind: int = 100
#     w: float = 0.6
#     pop_size: int = 100
#     neighbors: int = 10
#
#     def __post_init__(self):
#         global vehicle_capacity, n_vehicles, matrix, demands
#
#         self.problem = Instance().load_instance(self.path)
#         self.nodes = self.problem.dimension
#         vehicle_capacity = self.problem.capacity
#         n_vehicles = 5
#         matrix = self.problem.node_distances
#         demands = self.problem.node_demand
#         self.population = list()
#
#     def create_population(self):
#         self.population = [Individuo(size=self.nodes) for _ in range(self.pop_size)]
#
#
#     def velocity_calculate(self):
#         r1 = random.random()
#         r2 = random.random()
#         for ind in self.population:
#             ind.velocity = self.w * ind.velocity + (self.c1 * r1 * (ind.best_local['pos'] - ind.position)) \
#                            + (self.c2 * r2 * (ind.best_global['pos'] - ind.position))
#
#     def position_calculate(self):
#         for ind in self.population:
#             ind.position += ind.velocity
#
#     def fitness_calculate(self):
#         for ind in self.population:
#             ind.order_ind()
#             ind.fitness_calculate()
#
#     def best_local_actualize(self):
#         for ind in self.population:
#             if ind.fit < ind.best_local['fit']:
#                 ind.best_local = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
#
#     def best_global_neighbor_actualize(self):
#         """
#         :posicao 0 da população vai verificar do 0 até 0 19 e usar de global o de menor valor
#         posicao 1 vai olhar do 1 até 0 20
#         posicao 45 vai olhar o?
#         usar lógica básica pra fazer o anel, mas depois trocar pra modulo
#         """
#         i = 0
#         while i < self.pop_size:
#             if i - self.neighbors < 0:
#                 best_fit = self.population[i].best_global['fit'] if self.population[i].best_global is not None else self.population[i].fit
#                 best_ind = self.population[i].best_global
#                 start = self.pop_size + (i - self.neighbors)
#                 mid = 0
#                 end = i + self.neighbors
#
#                 for ind in self.population[start:]:
#                     if ind.best_local['fit'] < best_fit:
#                         best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
#                         best_fit = best_ind['fit']
#
#                 for ind in self.population[mid:end + 1]:
#                     if ind.best_local['fit'] < best_fit:
#                         best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
#                         best_fit = best_ind['fit']
#
#                 for ind in self.population[start:]:
#                     ind.best_global = best_ind
#
#                 for ind in self.population[mid: end + 1]:
#                     ind.best_global = best_ind
#                 i += 1
#                 print(i)
#
#             elif self.pop_size - i < self.neighbors:
#                 start = i - self.neighbors
#                 mid = 0
#                 end = self.neighbors - (self.pop_size - 1)
#                 for ind in self.population[start:mid + 1]:
#                     if ind.best_local['fit'] < best_fit:
#                         best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
#                         best_fit = best_ind['fit']
#
#                 for ind in self.population[mid: end + 1]:
#                     if ind.best_local['fit'] < best_fit:
#                         best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
#                         best_fit = best_ind['fit']
#
#                 for ind in self.population[start:mid + 1]:
#                     ind.best_global = best_ind
#
#                 for ind in self.population[mid: end + 1]:
#                     ind.best_global = best_ind
#                 i += 1
#                 print(i)
#
#             else:
#                 start = i - self.neighbors
#                 mid = i
#                 end = i + self.neighbors
#
#                 for ind in self.population[start:mid + 1]:
#                     if ind.best_local['fit'] < best_fit:
#                         best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
#                         best_fit = best_ind['fit']
#
#                 for ind in self.population[mid: end + 1]:
#                     if ind.best_local['fit'] < best_fit:
#                         best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
#                         best_fit = best_ind['fit']
#
#                 for ind in self.population[start:mid + 1]:
#                     ind.best_global = best_ind
#
#                 for ind in self.population[mid: end + 1]:
#                     ind.best_global = best_ind
#                 i += 1
#                 print(i)
#
#     def best_global(self, start = None):
#
#         if start:
#             best_global = self.population[0].fit
#             best_ind = self.population[0].best_local
#         else:
#             best_global = self.population[0].best_global['fit']
#             best_ind = self.population[0].best_global
#
#         for ind in self.population:
#             if ind.fit < best_global:
#                 best_ind = {'pos': ind.position, 'fit': ind.fit, 'route': ind.ind}
#                 best_global = ind.fit
#
#         for ind in self.population:
#             ind.best_global = best_ind




class Individuo(object):

    def __new__(cls, *args, **kwargs): #criar individuos diferentes por iteração
        return object.__new__(cls)

    def __init__(self, size):
       self.create_ind(size)

    def create_ind(self,size):
        self.ind = list(range(2, size+1))
        self.position = [random.random() for _ in range(len(self.ind))]
        self.order_ind()
        self.velocity = np.array([random.uniform(-2,2) for i in range(len(self.ind))])
        self.fitness_calculate()
        self.best_local = {'pos': self.position, 'fit': self.fit, 'route': self.ind}
        self.best_global = None

    def order_ind(self):
        indices = list(range(len(self.ind)))
        indices.sort(key=lambda i: self.position[i])
        self.ind = [self.ind[i] for i in indices]
        self.position = np.array([self.position[i] for i in indices])

    def fitness_calculate(self):
        routes = commons.define_routes(vetor=self.ind, demands=demands, vehicle_capacity=vehicle_capacity)
        self.fit = commons.dist_calculate(vet_aux=routes, matrix=matrix)

    def fitness(self):
        return self.fit #usado como lambda em funções


if __name__ == "__main__":
    path = "instances/A-n32-k5.txt"
    PSO = PSO(path=path)
    #PSO = PSO_Instance(path=path)
    PSO.create_population()
    PSO.best_global_actualize()
    iter = 100

    for i in range(iter):
        PSO.velocity_calculate()
        PSO.position_calculate()
        PSO.fitness_calculate()
        PSO.best_local_actualize()
        PSO.best_global_actualize()

        print(f' iteracao {i}')
    for ind in PSO.population:
        print(f'{ind.best_global["fit"]=} {ind.best_local["fit"]}')