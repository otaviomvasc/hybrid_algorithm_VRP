from random import *
import tsplib95
import numpy as np
from dataclasses import dataclass
import copy
import random
import math


@dataclass
class ReadTSPLIB:
    path: str

    def __post_init__(self):
        self.problem = tsplib95.load(self.path)

    def get_node_list(self):
        return np.array(list(self.problem.get_nodes()))

    def get_coords(self):
        return self.problem.as_name_dict()['node_coords']

    def get_matrix(self):
        nodes = self.get_node_list()
        coords = self.get_coords()
        matrix = [[np.ceil(np.linalg.norm(np.array((coords[i][0], coords[i][1]))-np.array((coords[j][0],coords[j][1])))) for j in nodes] for i in nodes]
        return np.matrix(matrix)

    def get_demands(self):
        return self.problem.as_name_dict()['demands']

    def get_vehicle_capacites(self):
        return self.problem.as_name_dict()['capacity']

    def get_number_of_vehicles(self):
        aux = self.problem.as_name_dict()['comment'].split(",")
        try:  #TODO: Will find one best way to get the number of vehicles!!
            return int(aux[1][19])
        except:
            return int(aux[0][19])


if __name__ == '__main__':
    path = 'eilb101.vrp.txt'
    problem = ReadTSPLIB(path)
    matrix = problem.get_matrix()
    number_of_vehicles = problem.get_number_of_vehicles()
    a=0
