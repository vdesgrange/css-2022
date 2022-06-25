import numpy as np
import copy

from constants import Coeff, State
from graphic_utils import visualize

class Device:
    def __init__(self, id, network):
        self.id = id
        self.network = network
        self.state = State.S
        self.t = 0
        self.tau = 0

    def omega(self):
        omega = 0
        neighbours = list(self.network.G.neighbors(self.id))
        for node_j in neighbours:
            if self.network.G.nodes[node_j]['data'].state == State.I:
                omega += 1

        return omega / len(neighbours)

    def X(self):
        omega = self.omega()
        p =[Coeff.H * omega, 1 - Coeff.H * omega]
        return np.random.choice([0, 1], None, p=p)

    def Y(self):
        return np.random.choice([0, 1, 2], None, p=[Coeff.A, Coeff.B, 1 - Coeff.A - Coeff.B])

    def Z(self):
        return np.random.choice([0, 1], None, p=[Coeff.Rs, 1 - Coeff.Rs])


    def step(self):
        self.t += 1
        self.tau += 1

        if self.state == State.S and self.X():
            self.state = State.I
            self.t = 0
            return

        if self.state == State.I and self.t > Coeff.T:
            y = self.Y()
            if y == 0:
                self.state = State.A
                self.tau = 0
            elif y == 1:
                self.state = State.S
            else:
                self.state = State.R
            return

        if self.state == State.A and self.tau > Coeff.Tau:
            self.t = 0
            self.tau = 0
            z = self.Z()
            if z:
                self.state = State.S
            else:
                self.state = State.R
            return

        return

# class CustomDevice:
#     def __init__(self, id, network, conf):
#         self.id = id
#         self.network = network
#         self.state = State.S
#         self.t = 0
#         self.tau = 0
#         self.conf = conf
#
#     def omega(self):
#         omega = 0
#         neighbours = list(self.network.G.neighbors(self.id))
#         for node_j in neighbours:
#             if self.network.G.nodes[node_j]['data'].state == State.I:
#                 omega += 1
#
#         return omega / len(neighbours)
#
#     def X(self):
#         omega = self.omega()
#         p =[Coeff.H * omega, 1 - Coeff.H * omega]
#         return np.random.choice([0, 1], None, p=p)
#
#     def step(self):
#         self.t += 1
#
#         if self.t > self.tau:
#             states = self.conf.transitions[self.state]
#             neighbours = list(self.network.G.neighbors(self.id))
#
#             p = self.conf.p[self.id][self.state]
#             self.state = np.random.choice(states, None, p=p)

def step(st_i, network, initial_nodes):
    """
    Step of the AMP model simulation
    :param st_i: step number
    :param net: graph class
    :return:
    """
    print("Step ", st_i)

    visited = set()
    to_visit = []
    to_visit.extend(list(initial_nodes))

    while to_visit:  # BFS
        node_i = to_visit.pop(0)
        if node_i not in visited:
            network.G.nodes[node_i]['data'].step()

            visited.add(node_i)
            neighbours = list(network.G.neighbors(node_i))
            to_visit.extend(neighbours)

    network.get_attributes()

    return network

def amp_model(network, max_iter, infected_ids, data=None):
    """
    AMP model main simulation thread
    :param network: networkx graph
    :param max_iter: number of epochs
    :param infected_ids: initial number of infected individual
    :param configured rules
    :return:
    """
    states_over_time = []
    next = network

    states_over_time.append(next.G.copy(as_view=False))

    # Set infected nodes
    source_neighbours = set()
    for id in infected_ids:
        source_neighbours = source_neighbours.union(set(network.G.neighbors(id)))
        network.G.nodes[id]['state'] = State.I
        network.G.nodes[id]['data'].state = State.I

    # Run simulation
    for i in range(max_iter):
        next = step(i, next, source_neighbours)
        source_neighbours = [np.random.choice(list(network.G.nodes))]
        states_over_time.append(copy.deepcopy(next.G.copy(as_view=False)))
        # visualize(next.G)

    return states_over_time
