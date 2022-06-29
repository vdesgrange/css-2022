import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy
from .constants import State

def regenerate_network(G, grid):
    H = copy.deepcopy(G)
    for u in grid.get_all_cell_contents():
        if (u.state == State.DEATH or u.state == State.OFFLINE): # State.RESISTANT
            # H.remove_node(u.unique_id)
            # Doing the same (+ one loop) depends if you want to also consider individual nodes.
            for v in grid.get_neighbors(u.unique_id, False):
                try:
                    H.remove_edge(u.unique_id, v)
                except nx.NetworkXError:
                    pass
    return H

def get_clusters(G):
    return nx.number_connected_components(G)

def get_clustering_coefficient(G):
    return nx.average_clustering(G)

def get_communities(G):
    # cc = nx.girvan_newman(G)
    # return cc
    pass

def get_degree_distribution(G):
    k = G.degree()
    hist = np.histogram(np.array([y for _,y in k]))
    return hist

def analyse_clusters(G):
    H = nx.connected_components(G)
    hist_cc = []
    min_cc = 0
    max_cc = 0

    if H is not None:
        cc = [len(c) for c in sorted(H, key=len, reverse=True)]
        min_cc = min(cc)
        max_cc = max(cc)
        bins = np.arange(min_cc, max_cc + 2, 1)
        hist_cc = np.histogram(np.array(cc), bins=bins)

    return (hist_cc, (min_cc, max_cc))

def time_analysis(timeline):
    healthy=[]
    exposed=[]
    infected=[]
    recovered=[]
    dead=[]

    for i in range(len(timeline)):
        G = timeline[i]
        temp = [G.nodes[id]['data'].state for id in list(G.nodes)]
        healthy.append(temp.count(0))
        exposed.append(temp.count(1))
        infected.append(temp.count(2))
        recovered.append(temp.count(3))
        dead.append(temp.count(4))

    x = np.linspace(0, len(timeline), len(timeline))
    plt.plot(x, healthy, 'o', color='blue')
    plt.plot(x, exposed, 'o', color='yellow')
    plt.plot(x, infected, 'o', color='red')
    plt.plot(x, recovered, 'o', color='green')
    plt.plot(x, dead, 'o', color='black')
    plt.show()

    return(healthy,exposed,recovered,infected,dead)

def cellular_automata_analysis(matrix):
    """
    Plot the evolution of graph has a 2D matrix
    :param matrix: t-by-n matrix representing agent state through time
    """
    pass

def shannon_entropy():
    """
    To adapt for discrete variable
    """
    pk = 0
    H = 0
    for _, p in enumerate(pk):
        if p > 0:
            H -= p * np.log(p)

