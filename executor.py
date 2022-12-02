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
    gen = 2350
    best_pop_size = 60
    best_news = 54


    all_data = list()
    same_repetitions = 30
    save_data = 200

    #parou na generation 350, news_iter 18 e pop_size 290
    cont_save_data=0
    rep = 0
    result_aux = list()
    row = 1
    #TODO: Use np.linspace
    generations_iter = [i for i in range(50, 3001, 50)]
    news_iter = [i for i in range(2, 50, 4)]
    pop_size_iter = [i for i in range(10, 301, 20)]
    for gen in generations_iter:
        for news in news_iter:
            for pop_size in pop_size_iter:
                print(gen, news, pop_size)

                while rep <= same_repetitions:
                    GA = GeneticAlgorithm(
                        path=path,
                        news=news,
                        generations=gen,
                        population_size=pop_size,
                        survivors=(best_pop_size / 2))
                    #TODO: Save one best_values per df line or save a list of best_fitness?
                    best_value = GA.genetic_algorithm(save=True)
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
#data = GA_analyze(path)


#T, alfa, max_times, number_executions = 1000, 0.5, 400, 200 #SA params
generations, news, population_size, survivors = 5, 100, 500, 200
#SA = SimulatedAnnealing(path=path, T=T, alfa=alfa, max_times=max_times)
start = time.time()

GA = GeneticAlgorithm(path=path, generations=generations, news=news, population_size=population_size, survivors=survivors)
i = 0
test_time = list()
while i < 1:
    print(i)
    best_dist = GA.genetic_algorithm(save=True)
    test_time.append(best_dist)
    i+= 1
#all_results, best_result = SA.multiple_executions(number_executions=number_executions, initial_solution=best_route)
print(f'menor resultado é: {min(test_time)}')
end = time.time()

print("The time of execution of above program is :", end-start)
