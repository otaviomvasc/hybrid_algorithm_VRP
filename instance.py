import math
import os.path


class Instance(object):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self):
        self.name = ""
        self.comment = ""
        self.dimension = 0
        self.capacity = 0
        self.type = ""
        self.nct = "NO_COORDS"
        self.ewt = ""
        self.ewf = ""
        self.edf = ""
        self.ddt = "NO_DISPLAY"

        self.node_coord = {}
        self.node_distances = {}
        self.node_demand = {}

    def __str__(self):
        return """Name: %s \nType : %s \nComment: %s \nNodes: %s \nDimension: %s \nCapacity: %s \nEdge weight: %s \nNode demand: %s \nNode coordinate type: %s \n""" % \
               (self.name, self.type, self.comment, self.node_coord, self.dimension, self.capacity, self.node_distances, self.node_demand, self.ewt)

    def load_instance(self, name):
        self.__init__()
        self.name = name
        with open(self.name) as f:
            while True:
                line = f.readline()
                (var, _, val) = line.partition(":")
                var = var.strip()
                val = val.strip()

                if var == "NAME":
                    self.name = val
                elif var == "TYPE":
                    self.type = val
                elif var == "COMMENT":
                    self.comment = val
                elif var == "DIMENSION":
                    self.dimension = int(val)
                elif var == "CAPACITY":
                    self.capacity = int(val)
                elif var == "EDGE_WEIGHT_TYPE":
                    self.ewt = val
                elif var == "EDGE_WEIGHT_FORMAT":
                    self.ewf = val
                elif var == "EDGE_DATA_FORMAT":
                    self.edf = val
                elif var == "NODE_COORD_TYPE":
                    self.nct = val
                elif var == "DISPLAY_DATA_TYPE":
                    self.ddt = val

                elif var == "NODE_COORD_SECTION":
                    self.node_coord = [(lambda x: (float(x[1]), float(x[2])))(f.readline().split()) for _ in range(self.dimension)]
                elif var == "DEMAND_SECTION":
                    self.node_demand = [(lambda x: float(x[1]))(f.readline().split()) for _ in range(self.dimension)]
                elif var == "EOF":
                    break
                elif var == "":
                    break
            return self.edge_weight()

    def edge_weight(self):
        if self.ewt == "EUC_2D":
            def distances(a, b):
                return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        else:
            def distances(a, b):
                return 0
        self.node_distances = [[distances(self.node_coord[i], self.node_coord[j]) for i in range(self.dimension)] for j in range(self.dimension)]
        return self

    def compute_vrp_routes(self, nodes):
        routes_list = []
        capacity_used = 0
        count = 1

        for i in nodes:
            if (capacity_used + self.node_demand[i-1]) <= self.capacity:
                capacity_used += self.node_demand[i-1]
                if i is nodes[-1]:
                    routes_list.append(count)
                    break
            else:
                if i is nodes[-1]:
                    routes_list.append(count - 1)
                    routes_list.append(1)
                    break
                count -= 1
                routes_list.append(count)
                capacity_used = self.node_demand[i-1]
                count = 1
            count += 1
        return routes_list

    def compute_vrp_distance(self, routes, nodes):
        starts = 0
        distance = 0
        for i in routes:
            total = 0
            total += self.node_distances[0][nodes[starts]-1]
            cont = starts
            while cont < starts + (i - 1):
                total += self.node_distances[nodes[cont] -1][nodes[cont + 1] -1]
                cont += 1
            total += self.node_distances[nodes[starts + (i - 1)]-1][0]
            starts += i
            distance += total
        return distance

    def compute_tsp_distance(self, nodes):
        total = 0
        for i in range(len(nodes)-1):
            total += self.node_distances[nodes[i]][nodes[i + 1]]
        total += self.node_distances[nodes[-1]][nodes[0]]
        return total