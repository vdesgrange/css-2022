from abm_network.simulations import simulations, simulate_barabasi_albert, simulate_max_fraction_iod
import statistics
import pandas as pd
import csv
import sys

def simulate_ba_spread(N = 10):

    """
    Topology: barabasi albert
    Run experiments to calculate fraction of affected nodes
    """
    
    max_spread = []

    for i in range(100):
        max_spread.append(simulate_barabasi_albert())

    avg = sum(max_spread)/len(max_spread)
    print(f"Average spread is {avg}")

    with open(f'data/max_avg_spread_N_BA.csv', 'w') as f: 
        write = csv.writer(f) 
        for i in max_spread:
            write.writerow([i]) 



def calculate_max_avg_spread(N = 10):

    """
    Topology: Erdos-Renyi
    Run experiments to calculate fraction of affected nodes
    """
    
    max_spread = []

    for i in range(100):
        max_spread.append(simulate_max_fraction_iod(N))

    avg = sum(max_spread)/len(max_spread)
    print(f"Average spread fraction is {avg}")

    with open(f'data/3_max_avg_spread_example_{N}_ER.csv', 'w') as f: 
        write = csv.writer(f) 
        for i in max_spread:
            write.writerow([i]) 

def calculate_max_avg_spread(N = 10):

    """
    Topology: Barabasi-Albert
    Run experiments to calculate fraction of affected nodes
    """

    max_spread = []

    for i in range(100):
        max_spread.append(simulate_max_fraction_iod(N))

    avg = sum(max_spread)/len(max_spread)
    print(f"Average spread fraction is {avg}")

    with open(f'data/BA_max_avg_spread_example_{N}_BA.csv', 'w') as f: 
        write = csv.writer(f) 
        for i in max_spread:
            write.writerow([i]) 


def simulate(N = 10, iterations = 1, k = 1):

    """
    Topology: Erdos-Renyi
    Run experiments to calculate fraction of affected nodes
    """

    results = []

    for i in range(iterations):
        results.append(simulations(N, k))

    for j, res in enumerate(results):

        with open(f'notebooks/data/av/ts_iod_{N}_ER_{j}_{k}.csv', 'w') as f: 
            write = csv.writer(f) 
            for l in res:
                write.writerow(l) 


if __name__ == "__main__":
    # Amount of nodes
    N = int(sys.argv[1])

    # Amount of iterations
    iterations = int(sys.argv[2])

    # Amount of nodes where infection starts
    k = int(sys.argv[3])

    # calculate_max_avg_spread(N = 1000)
    simulate(N, iterations, k)
