import mesa
from .model import VirusOnNetwork
from .parameters import analysis_params_a
import pandas as pd
import math
import time

iterations = 20
max_steps = 30

def experiment_a():

    global iterations 
    global max_steps

    results = mesa.batch_run(
        VirusOnNetwork,
        parameters=analysis_params_a,
        iterations = iterations,
        max_steps = max_steps,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    return results

def simulations():

    start = time.time()

    global iterations
    global max_steps

    results = experiment_a()

    res = {}
    logres = {}

    for i, result in enumerate(results):
        
        if result['Step'] is not max_steps:
            continue
        
        # print(i, result)

        nodes = result['num_nodes']
        # lognodes = math.log(nodes)

        if nodes not in res.keys():
            res[nodes] = 0

        # if lognodes not in logres.keys():
        #     logres[lognodes] = 0
        
        infected_offline_nodes = (int(result['Infected']) + int(result['Offline']))/ int(nodes) / iterations
        print(int(result['Infected']) + int(result['Offline']), int(nodes))
        res[nodes] += infected_offline_nodes
        # logres[lognodes] += math.log(infected_offline_nodes)

    print(res)
    # print(logres)
    end = time.time() - start
    print(end)



    #     # print(result['Susceptible'])
    #     # print(result['Resistant'])
    #     # print(result['Offline'])
    #     # print(result['Death'])


    # for i in ids.keys():
    #     _sum = 0
    #     for j in ids[i]:
    #         _sum += res[j]

    #     final =  math.log((_sum/(iterations*len(ids[i]))))
    #     # print(math.log(res['Ccoeff']))
    #     print(math.log(i), math.log(_sum/(iterations*len(ids[i]))))
    #     print(iterations, len(ids[i]))
    #     print(final)
    # # print(res)
    # print(ids)

