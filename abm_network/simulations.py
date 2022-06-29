import mesa
from .model import VirusOnNetwork
from .parameters import analysis_params_a
import pandas as pd
import math
import time
from .rule_functions import *

def input_sim(iterations = 1, max_steps = 50):

    return iterations, max_steps

def config2(N, k):

    targeted_ba = {
        "num_nodes": N,
        "avg_node_degree": 3,
        "initial_outbreak_size": k,
        "malware_spread_chance": malware_spread_chance,
        "malware_check_frequency":  malware_check_frequency,
        "recovery_chance":  recovery_chance,
        "gain_resistance_chance":  gain_resistance_chance,
        "susceptible_chance":  susceptible_chance,
        "death_chance":  death_chance,
        "centrality": "random",
        "network": "erdos-renyi"
    }

    return targeted_ba


def input_sim_2(iterations = 1, max_steps = 100):

    return iterations, max_steps


def experiment_a(N = 10, k = 1):

    iterations, max_steps = input_sim(1, 100)

    results = mesa.batch_run(
        VirusOnNetwork,
        parameters= config2(N, k),
        iterations = iterations,
        max_steps = max_steps,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    return max_steps, iterations, results


def config1(N):

    max_frac = {
        "num_nodes": N,
        "avg_node_degree": 3,
        "initial_outbreak_size": 1,
        "malware_spread_chance": malware_spread_chance,
        "malware_check_frequency":  malware_check_frequency,
        "recovery_chance":  recovery_chance,
        "gain_resistance_chance":  gain_resistance_chance,
        "susceptible_chance":  susceptible_chance,
        "death_chance":  death_chance,
        "centrality": "random",
        "network": "erdos-renyi"
    }

    return max_frac


def experiment_b(N = 10):

    iterations, max_steps = input_sim(1, 100)

    results = mesa.batch_run(
        VirusOnNetwork,
        parameters = config1(N),
        iterations = iterations,
        max_steps = max_steps,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    return max_steps, iterations, results


# def experiment_c(N = 10):

#     iterations, max_steps = input_sim(1, 100)

#     results = mesa.batch_run(
#         VirusOnNetwork,
#         parameters = config1(N),
#         iterations = iterations,
#         max_steps = max_steps,
#         number_processes=1,
#         data_collection_period=1,
#         display_progress=True,
#     )

#     return max_steps, iterations, results


def simulate_barabasi_albert(N = 10):

    start = time.time()
    max_steps, iterations, results = experiment_a(N)

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


def simulate_max_fraction_iod(N = 10):


    start = time.time()
    max_steps, iterations, results = experiment_b(N)

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

        off_inf_dea.append((int(result['Infected']) + int(result['Offline']) + int(result['Death']))/nodes)

        if nodes not in res.keys():
            res[nodes] = 0
        
        # infected_offline_nodes = (int(result['Infected']) + int(result['Offline']))/ int(nodes) / iterations
        # res[nodes] += infected_offline_nodes

    print(f"Max spread fraction at some point is {max(off_inf_dea)}")
    print(off_inf_dea)
    # print(logres)
    end = time.time() - start
    print(end)
    return max(off_inf_dea)


def simulate_antivirus(N = 10):

    start = time.time()
    max_steps, iterations, results = experiment_b(N)

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

        off_inf_dea.append((int(result['Infected']) + int(result['Offline']) + int(result['Death']))/nodes)

        if nodes not in res.keys():
            res[nodes] = 0
        
        # infected_offline_nodes = (int(result['Infected']) + int(result['Offline']))/ int(nodes) / iterations
        # res[nodes] += infected_offline_nodes

    print(f"Max spread fraction at some point is {max(off_inf_dea)}")
    print(off_inf_dea)
    # print(logres)
    end = time.time() - start
    print(end)
    return max(off_inf_dea)



def simulations(N = 50, k = 1):

    start = time.time()

    max_steps, iterations, results = experiment_a(N, k)

    res = {}
    r = []

    for i, result in enumerate(results):

        nodes = result['num_nodes']

        if nodes not in res.keys():
            res[nodes] = 0

        
        infected_offline_nodes = (int(result['Infected']) + int(result['Offline']) + int(result['Death']))
        r.append([result['Step'], infected_offline_nodes])

    end = time.time() - start
    print(end)
    return r
