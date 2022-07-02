import mesa
from .model import VirusOnNetwork
from .parameters import analysis_params_a
import pandas as pd
import math
import time
from .rule_functions import *

def input_sim(iterations = 1, max_steps = 50):

    return iterations, max_steps

targeted_ba = {
    "num_nodes": [1000],
    "avg_node_degree": 3,
    "initial_outbreak_size": 1,
    "malware_spread_chance": malware_spread_chance,
    "malware_check_frequency":  malware_check_frequency,
    "recovery_chance":  recovery_chance,
    "gain_resistance_chance":  gain_resistance_chance,
    "susceptible_chance":  susceptible_chance,
    "death_chance":  death_chance,
    "centrality": "random",
    "network": "Barabasi-Albert"
}


def experiment_a():
<<<<<<< HEAD:abm_network/simulations.py

    iterations, max_steps = input_sim(1, 100)
=======
    """
    Example of mesa batch_run usage to perform simulation analysis
    """
    global iterations 
    global max_steps
>>>>>>> 21342aa8d8bccb494fa8227c2f6698a343fc0ed7:SIROD/abm_network/simulations.py

    results = mesa.batch_run(
        VirusOnNetwork,
        parameters= targeted_ba,
        iterations = iterations,
        max_steps = max_steps,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    return max_steps, iterations, results


def simulate_barabasi_albert():

    start = time.time()
    max_steps, iterations, results = experiment_a()

    res = {}
    off_inf_dea = []

    for i, result in enumerate(results):
        
        # if result['Step'] is not max_steps:
        #     continue

        nodes = result['num_nodes']
        print(f"Step: {i}")
        print(nodes, result['Resistant'])
        print(nodes, result['Infected'])
        print(nodes, result['Susceptible'])
        print(nodes, result['Offline'])

        off_inf_dea.append(int(result['Infected']) + int(result['Offline'] + int(result['Death'])))

        if nodes not in res.keys():
            res[nodes] = 0
        
        infected_offline_nodes = (int(result['Infected']) + int(result['Offline']))/ int(nodes) / iterations
        res[nodes] += infected_offline_nodes

    print(res)
    print(f"Max spread at some point is {max(off_inf_dea)}")
    print(off_inf_dea)
    # print(logres)
    end = time.time() - start
    print(end)
    return max(off_inf_dea)


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
        # print(int(result['Infected']) + int(result['Offline']), int(nodes))
        res[nodes] += infected_offline_nodes

    print(res)
    end = time.time() - start
    print(end)
<<<<<<< HEAD:abm_network/simulations.py
=======

>>>>>>> 21342aa8d8bccb494fa8227c2f6698a343fc0ed7:SIROD/abm_network/simulations.py
