from reader_tspLIB import ReadTSPLIB
from simulated_annealing import SimulatedAnnealing
from genetic_algorith import GeneticAlgorithm
from itertools import permutations
from collections import defaultdict
import pandas as pd
import numpy as np
import time

def GA_analyze(path):

    #Analises individuais dos parametros, com base em mil gerações!!
    # generations  = [100, 3001 - 100 em 100}
    # n_individuos = 0.1 - 1 da qntd de individuos 0.1 - 0.1
    # pop = 50 - 500 50/50
    cont_save_data=0

    result_aux = list()
    #TODO: usar np.seed

    rep = 0
    all_data = list()
    same_repetitions = 30
    save_data = 30
    generations_iter = np.arange(100, 3001, 100)
    news_iter = np.arange(0.1, 1.01, 0.1)
    pop_size_iter = np.arange(50, 501, 50)
    for gen in generations_iter:
        for news in news_iter:
            for pop_size in pop_size_iter:
                print(gen, news*gen, pop_size)

                while rep <= same_repetitions:
                    GA = GeneticAlgorithm(
                        path=path,
                        news=int(news * gen),
                        generations=gen,
                        population_size=pop_size,
                        survivors=int(pop_size / 2))
                    best_value, _ = GA.genetic_algorithm()

                    result_aux.append(best_value)
                    rep += 1


                result = {'generations': gen, 'news': news, 'population': pop_size, "best_value": result_aux[:]}
                all_data.append(result)
                cont_save_data += 1
                rep = 0
                result_aux.clear()
                if cont_save_data == save_data:
                    df = pd.DataFrame(all_data)
                    with pd.ExcelWriter('dados.xlsx', engine="openpyxl", mode='a', if_sheet_exists="replace") as writer:
                        df.to_excel(writer, 'Planilha')
                    cont_save_data = 0

    a=0


path = "instances/eil51.vrp..txt"
GA = GeneticAlgorithm(
                        path=path,
                        news=50,
                        generations=400,
                        population_size=200,
                        survivors=int(200 / 2))

SA = SimulatedAnnealing(path=path)
best_value, best_pop = GA.genetic_algorithm()
vector, best_rote, e_base = SA.simulated_annealing(initial_solution=best_pop)

print(best_value, e_base)





