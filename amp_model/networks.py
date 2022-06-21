import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from abc import ABC
from networkx.drawing.nx_agraph import graphviz_layout
from constants import COLORMAP
from graphic_utils import visualize


class Network(ABC):
    """
    Generic graph class
    """
    def __init__(self):
        self.G = nx.Graph()
        self.predecessor = None
        self.min_distances = None
        self.N = 0
        self.E = np.Inf
        self.L = None
        self.C = None
        self.alpha = 1  # tolerance parameter

    def floyd_warshall(self, key):
        """
        Floyd warshall to get matrix of most efficient path between 2 nodes
        Store path reconstruction
        Compute number of most efficient path going through node i at the current step
        :param key:
        :return:
        """
        dist = np.Inf * np.ones((self.N, self.N))
        pred = -1 * np.ones((self.N, self.N), dtype=np.uint8)

        for edge in self.G.edges:
            dist[edge[0], edge[1]] = self.G.edges[edge[0], edge[1]][key]
            dist[edge[1], edge[0]] = self.G.edges[edge[0], edge[1]][key]

            pred[edge[0], edge[1]] = edge[1]
            pred[edge[1], edge[0]] = edge[0]

        for node in list(self.G.nodes):
            dist[node, node] = 0
            pred[node, node] = node

        for k in list(self.G.nodes):
            for i in list(self.G.nodes):
                for j in list(self.G.nodes):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[i][k]

        return pred, dist

    def set_node(self, i, key, value):
        """
        Set a value to one edge of the network
        :param i: node i
        :param key: Key
        :param value: value
        """
        self.G.nodes[i][key] = value

    def random_assignment(self, p=0.1):
        nodes = list(self.G.nodes)
        infected = np.random.choice(nodes, round(len(nodes) * p))

        for node_id in nodes:
            if node_id in infected:
                self.G.nodes[node_id]['state'] = 'I'
            else:
                self.G.nodes[node_id]['state'] = 'S'

    def set_edges(self, key, value):
        """
        Set a value to all edges of the network
        :param key: Key
        :param value: value
        """
        for edge in self.G.edges:
            self.G.edges[edge[0], edge[1]][key] = value

    def set_edge(self, i, j, key, value):
        """
        Set a value to one edge of the network
        :param i: node i
        :param j: node j
        :param key: Key
        :param value: value
        """
        self.G.edges[i, j][key] = value

    def get_num_paths(self, predecessor):
        """
        Determine number of most efficient path going through each node
        :return:
        """
        n_spaths = np.zeros(self.N)
        for source in self.G:
            for dest in self.G:
                curr_node = source
                while curr_node != dest:
                    n_spaths[curr_node] += 1
                    curr_node = predecessor[curr_node][dest]

        return n_spaths

    def get_attributes(self):
        # Get parameters
        self.predecessor, self.min_distances = self.floyd_warshall(key='flow')
        curr_N = self.G.number_of_nodes()
        D = np.nansum(np.true_divide(1, self.min_distances, out=np.zeros_like(self.min_distances), where=self.min_distances != 0))
        self.E = (1 / (curr_N * (curr_N - 1))) * (D / 2)
        self.L = self.get_num_paths(self.predecessor)

        return self.predecessor, self.min_distances, self.E, self.L

    def remove_node(self, id=-1):
        rnd_id = id if id != -1 else np.random.choice(list(self.G.nodes))
        self.G.remove_node(rnd_id)
        self.L[rnd_id] = 0
        self.C[rnd_id] = 0


class Tree_Network(Network):
    """
    Tree-like graph
    """
    def __init__(self, branching_c, height_h, alpha):
        super().__init__()
        self.h = height_h
        self.c = branching_c
        self.node_id = branching_c + 2
        self.all_leaves = []
        self.alpha = alpha

        # Initialise Tree graph
        self.G.add_node(0)
        leaves = range(1, branching_c + 2)
        self.G.add_nodes_from(leaves)
        self.G.add_edges_from([(0, i) for i in leaves])
        self.generate(leaves, self.h)
        self.G.add_edges_from([(self.all_leaves[i-1], self.all_leaves[i]) for i in range(len(self.all_leaves))])
        self.random_assignment()
        self.set_edges('flow', 1)
        self.N = self.G.number_of_nodes()  # Initial number of nodes

        # Get parameters
        self.get_attributes()
        self.C = self.alpha * np.copy(self.L)

    def generate(self, leaves, h):
        """
        Generate a tree-like graph with set of default leaves and height h.
        :param leaves: default leaves
        :param h: height
        """
        if h <= 0:
            self.all_leaves.extend(leaves)
            return

        for leaf in leaves:
            new_leaves = []
            for i in range(self.c):
                new_leaves.append(self.node_id)
                self.G.add_node(self.node_id)
                # self.G.nodes[self.node_id]['bus_type'] = 'load'

                self.G.add_edge(leaf, self.node_id)
                self.node_id += 1

            self.generate(new_leaves, h - 1)

    def visualize(self):
        """
        Simple visualization tool of the tree graph
        """
        pos = graphviz_layout(self.G, prog="twopi", args="")
        node_color = [COLORMAP[self.G.nodes[id]['state']] for id in list(self.G.nodes)]
        plt.figure(figsize=(8, 8))
        nx.draw(self.G,
                pos,
                node_size=1000,
                alpha=0.7,
                node_color=node_color,
                with_labels=True)
        plt.axis("equal")
        plt.show()


class Barabasi_Albert_Network(Network):
    """
    Barabasi-Albert scale-free network
    """
    def __init__(self, n, m, alpha):
        super().__init__()
        self.n = n  # number of nodes
        self.m = m # number of edge to attach
        self.alpha = alpha
        self.all_leaves = []

        # Initialise Tree graph
        self.G = nx.barabasi_albert_graph(self.n, self.m)
        self.random_assignment()
        self.set_edges('flow', 1)
        self.N = self.G.number_of_nodes()  # initial number of nodes

        # Get parameters
        self.get_attributes()
        self.C = self.alpha * np.copy(self.L)

    def visualize(self):
        """
        Simple visualization tool of the graph
        """
        pos = graphviz_layout(self.G, prog="twopi", args="")
        node_color = [COLORMAP[self.G.nodes[id]['state']] for id in list(self.G.nodes)]
        plt.figure(figsize=(8, 8))
        nx.draw(self.G,
                pos,
                node_size=1000,
                alpha=0.7,
                node_color=node_color,
                with_labels=True)
        plt.axis("equal")
        plt.show()


if __name__ == '__main__':
    tree = Barabasi_Albert_Network(20, 10)
    visualize(tree.G)
    print("Tree ", len(tree.G.nodes))
