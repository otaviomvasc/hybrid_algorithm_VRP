from reader_tspLIB import ReadTSPLIB
from simulated_annealing import SimulatedAnnealing
from itertools import permutations
from collections import defaultdict
import pandas as pd
import numpy as np
import time
from GA_SA import Hibryd_Genetic_Algorithm
import time
import os

def GA_analyze():

    #Analises individuais dos parametros, com base em mil gerações!!
    # generations  = [100, 3001 - 100 em 100}
    # n_individuos = 0.1 - 1 da qntd de individuos 0.1 - 0.1
    # pop = 50 - 500 50/50
    cont_save_data=0

    result_aux = list()
    time_aux = list()
    #TODO: usar np.seed

    rep = 0
    all_data = list()
    same_repetitions = 10
    save_data = 20
    generations_iter = np.arange(100, 1500, 500)
    news_iter = np.arange(0.1, 1.01, 0.4)
    pop_size_iter = np.arange(50, 501, 150)
    SA_T = np.arange(1000, 10001, 5000)
    SA_alfa = np.arange(0.05, 0.999, 0.5)
    paths = ['instances/F-n135-k7.txt','instances/A-n63-k9.txt', 'instances/A-n33-k6.txt']
    for path in paths: #TODO: TROCA ISSO PELO ITERTOOLS PELO AMOR DE DEUS!!!!
        for gen in generations_iter:
            for news in news_iter:
                for pop_size in pop_size_iter:
                    for t in SA_T:
                        for alfa in SA_alfa:
                            print(gen, news*gen, pop_size, t, alfa, path)
                            while rep <= same_repetitions:
                                inicio = time.time()
                                GA = Hibryd_Genetic_Algorithm(
                                    path=path,
                                    news=int(news * gen),
                                    generations=gen,
                                    population_size=pop_size,
                                    survivors=int(pop_size / 2),
                                    T_SA=t,
                                    alfa_SA=alfa)

                                best_value, _ = GA.genetic_algorithm()
                                fim = time.time()
                                t_t = fim-inicio
                                result_aux.append(best_value)
                                time_aux.append((t_t))
                                rep += 1
                                print(rep)

                            result = {'generations': gen, 'news': news, 'population': pop_size, "SA_T": t, "SA_alfa": alfa, "best_value": result_aux[:], "time": time_aux[:]}
                            all_data.append(result)
                            cont_save_data += 1
                            rep = 0
                            result_aux.clear()
                            time_aux.clear()
                            if cont_save_data == save_data:
                                df = pd.DataFrame(all_data)
                                with pd.ExcelWriter('dados_GA_SA.xlsx', engine="openpyxl", mode='a', if_sheet_exists="replace") as writer:
                                    df.to_excel(writer, 'Planilha')
                                cont_save_data = 0

def compute_results():
    result_aux = list()
    time_aux = list()
    same_execution = 1
    data = list()
    for p in os.listdir("all_instances"):
        print(f'{p = }')
        path = "all_instances/" + p
        for _ in range(same_execution):
            print(f'{_ = }')
            inicio = time.time()
            try:
                GA_SA = Hibryd_Genetic_Algorithm(path=path)
                best_value, ____ = GA_SA.genetic_algorithm()
            except:
                continue
            fim = time.time()
            t_t = fim - inicio
            result_aux.append(best_value)
            time_aux.append((t_t))

        best_result = min(result_aux)
        corresp_time = time_aux[result_aux.index(best_result)]

        try:
            value_i = GA_SA.problem.problem.comment.find("value") + 7
            optimal_str = GA_SA.problem.problem.comment[value_i:]
            end_best_value = optimal_str.find(")")
            optimal_value = optimal_str[:end_best_value]
            m = ((best_result - int(optimal_value) )/int(optimal_value)) * 100
        except:
            m = 'otimo nao encontrado'
        result = {'instance': p, "optimal_value": optimal_value,  "best_value": best_result, "time": corresp_time, "gap": m}
        data.append(result)
        df = pd.DataFrame(data)
        result_aux.clear()
        time_aux.clear()
        with pd.ExcelWriter('resultados.xlsx', engine="openpyxl", mode='a', if_sheet_exists="replace") as writer:
            df.to_excel(writer, 'Planilha')
        b=0

if __name__ == "__main__":
    #GA_analyze()
    compute_results()