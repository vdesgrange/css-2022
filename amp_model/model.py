import numpy as np

from constants import COEFF, STATES

class Device:
    def __init__(self, id, network):
        self.id = id
        self.network = network
        self.state = STATES["S"]
        self.t = 0
        self.tau = 0

    def omega(self):
        omega = 0
        neighbours = list(self.network.G.neighbors(self.id))
        for node_j in neighbours:
            if node_j['class'].state == STATES["I"]:
                omega += 1

        return omega

    def X(self):
        omega = self.omega()
        p =[COEFF["H"] * omega, 1 - COEFF["H"] * omega]
        return np.random.choice(1, None, p=p)

    def Y(self):
        return np.random.choice(2, None, p=[COEFF["A"], COEFF["B"], 1 - COEFF["A"] - COEFF["B"]])

    def Z(self):
        return np.random.choice(1, None, p=[COEFF["Rs"], 1 - COEFF["Rs"]])


    def step(self):
        self.t += 1
        self.tau += 1

        if self.state == STATES["S"] and self.X():
            self.state = STATES["I"]
            self.t = 0
            return

        if self.state == STATES["I"] and self.t > COEFF["T"]:
            y = self.Y()
            if y == 0:
                self.state = STATES["A"]
                self.tau = 0
            elif y == 1:
                self.state = STATES["S"]
            else:
                self.state = STATES["R"]
            return

        if self.state == STATES["A"] and self.tau > COEFF["Tau"]:
            self.t = 0
            self.tau = 0
            z = self.Z()
            if z:
                self.state = STATES["S"]
            else:
                self.state = STATES["R"]
            return

        return

def loop(st_i, network, initial_nodes):
    """
    Step of the AMP model simulation
    :param st_i: step number
    :param net: graph class
    :return:
    """
    visited = set()  # Node visited
    to_visit = []  # Node to visit
    to_visit.extend(list(initial_nodes))

    while to_visit:  # BFS
        node_i = to_visit.pop(0)
        if node_i not in visited:
            network.G.node[node_i]['class'].step()

            visited.add(node_i)
            neighbours = list(network.G.neighbors(node_i))
            to_visit.extend(neighbours)

    network.get_attributes()

    return network

def run(network, max_iter, infected_ids):
    next = network

    # Set infected nodes
    source_neighbours = set()
    for id in infected_ids:
        source_neighbours = source_neighbours.union(set(network.G.neighbors(id)))
        network.node[id]['class'].state = COEFF["I"]

    # Redistribute flow
    for i in range(max_iter):
        next = loop(i, next, source_neighbours)
        source_neighbours = [np.random.choice(list(network.G.nodes))]

    return
