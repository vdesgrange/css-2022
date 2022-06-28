import mesa
from .model import VirusOnNetwork
from .parameters import analysis_params_a
import pandas as pd
import math
import time


def experiment(iterations = 10, max_steps = 100, number_processes = 1, data_collcetion_period = 1, display_progress = True):

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

    iterations = 10
    max_steps = 100
    start = time.time()
    results = experiment(iterations, max_steps)

    res = {}

    for i, result in enumerate(results):
        
        if result['Step'] is not max_steps:
            continue

        nodes = result['num_nodes']

        if nodes not in res.keys():
            res[nodes] = 0
        
        # infected_offline_nodes = (int(result['Infected']) + int(result['Offline']))

        # print(infected_offline_nodes)
        # res[nodes] += infected_offline_nodes
        res[nodes] += int(result['Resistant'])
        # res[nodes] += infected_offline_nodes

    print(res)
    end = time.time() - start
    print("Execution took " + str(end) + " seconds")


def simulations_until_resistant():

    iterations = 1
    max_steps = 100
    start = time.time()
    results = experiment(iterations, max_steps)

    res = {}

    for i, result in enumerate(results):

        # print(result)
        
        if result['Resistant'] == result['num_nodes']:
            print(result['num_nodes'], result['Step'])
            break

        nodes = result['num_nodes']

        if nodes not in res.keys():
            res[nodes] = 0

        if int(result['Resistant']) > 0:
            print(f"Antivirus at {result['Step']}")
            return result['Step']

        
        # infected_offline_nodes = (int(result['Infected']) + int(result['Offline']))
        # print(infected_offline_nodes)
        # res[nodes] += infected_offline_nodes

        if result['Step'] == max_steps:
            res[nodes] += int(result['Resistant'])

        # res[nodes] += infected_offline_nodes

    # print(res)
    end = time.time() - start
    print("Execution took " + str(end) + " seconds")
    # print(collect)
    return result['Step']


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


# def simulate_():

#     start = time.time()

#     global iterations
#     global max_steps

#     results = experiment_a()

#     res = {}

#     for i, result in enumerate(results):
        
#         if result['Step'] is not max_steps:
#             continue

#         nodes = result['num_nodes']

#         if nodes not in res.keys():
#             res[nodes] = 0
        
#         infected_offline_nodes = (int(result['Infected']) + int(result['Offline']))/ int(nodes) / iterations
#         res[nodes] += infected_offline_nodes

#     print(res)
#     end = time.time() - start
#     print("Execution took " + str(end) + " seconds")

