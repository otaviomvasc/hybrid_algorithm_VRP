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
            position = [random.uniform(0,1) for i in range(1,size)]
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

    def velocity_calculate(self): #TODO: will Velocity interval one parameter?
        return np.array([random.uniform(-4.0,4.0) for i in range(len(self.ind))])

    def new_position(self):
        pass

if __name__ == "__main__":
    path = "instances/eil23.vrp.txt"

    problem = ReadTSPLIB(path=path)
    vehicle_capacity = problem.get_vehicle_capacites()
    n_vehicles = problem.get_number_of_vehicles()
    matrix = problem.get_matrix()
    demands = problem.get_demands()
    coords = problem.get_coords()
    nodes = problem.get_node_list()
    pop = 50
    generations = 100
    c1r1 = 0.8
    c2r2 = 0.8


    population = [Individuo(size=len(nodes)) for i in range(pop)]
    g_best = min([p.fitness() for p in population])
    best = [p for p in population if p.fitness() == g_best]

    #isso vai ser feito já no init!!
    population[0].position = population[0].position + population[0].velocity
    population[0].order_per_position()
    population[0].fitness_calculation(demands, vehicle_capacity, matrix)
    population[0].best_local_actualize()
    g_best = min([p.fitness() for p in population])
    best = [p for p in population if p.fitness() == g_best]

    population[0].velocity = [population[0].velocity[i] + c1r1 * (population[0].best_local.position[i] - population[0].position[i]) + c2r2 * (
                best[0].position[i] - population[0].position[i]) for i in range(len(population[0].ind))]





    """
    criar classe individuo, que cria um vetor com a rota, outro com a velocidade, outro com a dimensao (confirmar nome) e o fitness
    utilizando o metodo new
    
    defino g_best
    
    while True:
        calculo nova velocidade de cada individuo
        calculo a posição de cada individuo
            função sigmoide de probabilidade 
        
        ordeno cada individuo de acordo com a position de forma decrescente - Confirmar isso
        calculo fitness
        
        redefino o g_best
        
    Dúvidas:
        na hora de calcular a posição eu uso o gbest e o pbest ou os valores aleatórios do position??
    """




