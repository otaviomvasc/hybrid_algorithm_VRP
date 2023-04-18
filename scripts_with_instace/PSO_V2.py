"""
Pseudo-código para testar lógica da PSO e conversão do PSO usando função da literatura

função f(x) = x sen (10 * pi * x) + 1 (máximo)
1 - criar população de individuos com valor f(x) aleatório
        criar melhor ótimo local de cada individuo, sendo o primeiro valor o inicial

2 - criar velocidades aleatórias

3 - Selecionar g_best (melhor valor global)

iterar geração
    iterar individuos:
        calculo nova velocidade
        calculo nova posição (x)
        calculo o novo fitness de acordo com a posição f(x)
        atualizo melhor ótimo local

    atualizo o melhor ótimo global
"""

import random
import numpy as np
import math


class Individuo(object):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self):
        self.position = random.uniform(-1,2)
        self.velocity = random.uniform(-1,1)
        self.fitness_calculate()
        self.best_local = self.position

    def fitness_calculate(self, x=None):
        """
        function x sen (10 * pi * x) + 1
        """
        if x is None:
            fit = math.sin((10 * math.pi * self.position)) * self.position + 1
            self.fitness = fit
        else:
            fit = math.sin((10 * math.pi * x)) * x + 1
            return fit

    def att_best_local(self):
        if self.fit() > self.fitness_calculate(self.best_local):
            self.best_local = self.position

    def velocity_calculate(self, c1, c2, r1, r2, w, best_global):
        self.velocity = w * self.velocity + (c1 * r1 * (self.best_local - self.position)) + (c2 * r2 * (best_global - self.position))

    def position_calculation(self):
        self.position += self.velocity
        #se a nova posicao estiver fora do meu limte a nova posição vai ser o reflexo (bolinha batendo no quadrado)

    def fit(self):
        return self.fitness

class Population():
    def __init__(self, pop):
        self.population=list()
        self.population_generation(pop=pop)


    def population_generation(self, pop):
        self.population = [Individuo() for i in range(pop)]


    def best_calculate(self):
        self.population = sorted(self.population, key=Individuo.fit, reverse=True)
        return self.population[0].position


iter = 100
c1, c2 = 1.2, 1.2
len_pop = 100
i=0
w = 0.8

pop = Population(pop=len_pop)
print(f'{i=}: {pop.population[0].fitness=} e {pop.population[0].position=}')


for i in range(iter):
    r1 = random.uniform(0,1)
    r2 = random.uniform(0,1)
    best_global = pop.best_calculate()
    for ind in pop.population:
        ind.position_calculation()
        ind.velocity_calculate(c1=c1, c2=c2, r1=r1, r2=r2, w=w, best_global=best_global)
        ind.fitness_calculate()
        ind.att_best_local()
        if ind.fit() > ind.fitness_calculate(best_global):
            best_global = ind.position

    print(f'{i=}: {pop.population[0].fitness_calculate(best_global)} e {best_global=}')


best_global = pop.best_calculate()
a=0




