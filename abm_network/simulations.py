import mesa
from .model import VirusOnNetwork
from .parameters import analysis_params_a
import pandas as pd
import math
import time

iterations = 20
max_steps = 30

def experiment_a():
    """
    Example of mesa batch_run usage to perform simulation analysis
    """
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
    """
    Example of mesa batch_run usage to perform simulation analysis
    In this case, analyse ratio of infected and offlines agents in comparison to all nodes.
    """

    global iterations
    global max_steps

    start = time.time()
    results = experiment_a()
    res = {}

    for _, result in enumerate(results):
        
        if result['Step'] is not max_steps:
            continue
        
        nodes = result['num_nodes']

        if nodes not in res.keys():
            res[nodes] = 0
        
        infected_offline_nodes = (int(result['Infected']) + int(result['Offline']))/ int(nodes) / iterations
        print(int(result['Infected']) + int(result['Offline']), int(nodes))
        res[nodes] += infected_offline_nodes

    print(res)
    end = time.time() - start
    print(end)

