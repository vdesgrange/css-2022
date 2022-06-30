import numpy as np
import networkx as nx
import copy
from .constants import State

def regenerate_network(G, grid):
    """
    Generate current state of the network
    """
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
    """
    Get sub-component of the graph G
    """
    return nx.number_connected_components(G)

def get_clustering_coefficient(G):
    """
    Compute clustering coefficient of graph G
    """
    return nx.average_clustering(G)

def get_degree_distribution(G):
    """
    Compute degree distribution of graph G
    """
    k = G.degree()
    hist = np.histogram(np.array([y for _,y in k]))
    return hist

def analyse_clusters(G):
    """
    Get distribution of sub-component size in network G
    """
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
