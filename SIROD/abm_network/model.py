import math
import random
import networkx as nx
import mesa
from mesa.model import Model
from .constants import State
from .agents import MalwareAgent
<<<<<<< HEAD:abm_network/model.py
from .analysis import regenerate_network, get_clusters, get_clustering_coefficient
from networkx import path_graph, random_layout
import copy
=======
from .analysis import *

>>>>>>> 21342aa8d8bccb494fa8227c2f6698a343fc0ed7:SIROD/abm_network/model.py


def number_state(model, state):
    """
    Return number of states
    :param model: Mesa model
    :param state: agent state
    :return int: number of agent in the given state
    """
    return sum(1 for a in model.grid.get_all_cell_contents() if a.state is state)


def number_infected(model):
    """
    Get number of INFECTED
    :param model: Mesa model
    :return int: number of agent in the infected state
    """
    return number_state(model, State.INFECTED)


def number_susceptible(model):
    """
    Get number of SUSCEPTIBLE
    :param model: Mesa model
    :return int: number of agent in the susceptible state
    """
    return number_state(model, State.SUSCEPTIBLE)


def number_resistant(model):
    """
    Get number of RESISTANT
    :param model: Mesa model
    :return int: number of agent in the resistant state
    """
    return number_state(model, State.RESISTANT)


def number_offline(model):
    """
    Get number of OFFLINE
    :param model: Mesa model
    :return int: number of agent in the offline state
    """
    return number_state(model, State.OFFLINE)


def number_death(model):
    """
    Get number of DEATH
    """
    return number_state(model, State.DEATH)


def number_clusters(model):
    """
    Generate graph with offline/dead node removed 
    then get number of components
    """

    H = regenerate_network(model.G, model.grid)
    return get_clusters(H)

def clustering_coeff(model):
    """
    Generate graph with offline/dead node removed 
    then compute clustering coefficient
    """

    H = regenerate_network(model.G, model.grid)
    return get_clustering_coefficient(H)

def cluster_distribution(model):
    """
    Get cluster size distribution
    """
    H = regenerate_network(model.G, model.grid)
    return analyse_clusters(H)



class VirusOnNetwork(Model):
    """A malware model with some number of agents"""

    def __init__(
        self,
        num_nodes=30,
        avg_node_degree=3,
        initial_outbreak_size=3,
        centrality="random",
        malware_spread_chance=0.4,
        malware_check_frequency=0.4,
        recovery_chance=0.3,
        gain_resistance_chance=0.5,
        network="erdos-renyi",
        matrix = [],
        importance = lambda : random.uniform(0, 1),
        susceptible_chance = 0.01,
        death_chance = 0.01,
    ):

        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = self.get_network(network, prob)
        self.k_max = max([d for _, d in self.G.degree()])
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.RandomActivation(self)
        self.initial_outbreak_size = (
            initial_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes
        )
        self.centrality = centrality
        self.malware_spread_chance = malware_spread_chance
        self.malware_check_frequency = malware_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance
        self.matrix = matrix
        self.importance = importance
        self.susceptible_chance = susceptible_chance
        self.death_chance = death_chance

        self.datacollector = mesa.DataCollector(
            {
                "Infected": number_infected,
                "Susceptible": number_susceptible,
                "Resistant": number_resistant,
                "Offline": number_offline,
                "Death": number_death,
                "Clusters": number_clusters,
                "Ccoeff": clustering_coeff,
                "Cluster_distribution": cluster_distribution,
            }
        )

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            a = MalwareAgent(
                i,
                self,
                State.SUSCEPTIBLE,
                self.malware_spread_chance,
                self.malware_check_frequency,
                self.recovery_chance,
                self.gain_resistance_chance,
                self.importance(),
                self.susceptible_chance,
                self.death_chance
            )
            self.schedule.add(a)
            # Add the agent to the node
            self.grid.place_agent(a, node)

        # Infect some nodes
        infected_nodes = self.set_initial_outbreak(initial_outbreak_size, centrality, descending = True)

        for a in self.grid.get_cell_list_contents(infected_nodes):
            if a != None:
                a.state = State.INFECTED

        self.running = True
        self.datacollector.collect(self)

    def get_network(self, network, prob):
        """
        Initialise network graph
        :param network: network type
        :param prob: connexion probability 
        :return graph
        """
        if network.lower() == "erdos-renyi":
            return nx.erdos_renyi_graph(n = self.num_nodes, p = prob, seed = 42)

        elif network.lower() == "barabasi-albert":
            return nx.barabasi_albert_graph(n = self.num_nodes, m = 1, seed = 42)

        else:
            return nx.watts_strogatz_graph(n = self.num_nodes, k = int(0.2*(self.num_nodes)), p = prob, seed = 42)


    def set_initial_outbreak(self, initial_outbreak_size, centrality = "random", descending = True):
        """
        Set initial outbreak nodes
        :param initial_outbreak_size: size of the initial outbreak
        :param centrality: type of centrality for initial outbreak: None == random, degree, closeness, betweennes
        :return array: list of node id
        """

        if centrality == 'random':
            return self.random.sample(list(self.G), self.initial_outbreak_size)

        elif centrality == "degree":
            degree = sorted(nx.degree_centrality(self.G).items(), key=lambda x:x[1], reverse = descending)
            return [i[0] for i in degree][:initial_outbreak_size]

        elif centrality == "closeness":
            closeness = sorted(nx.closeness_centrality(self.G).items(), key=lambda x:x[1], reverse = descending)
            return [i[0] for i in closeness][:initial_outbreak_size]

        elif centrality == "betweenness":
            betweenness = sorted(nx.betweenness_centrality(self.G).items(), key=lambda x:x[1], reverse = descending)
            return [i[0] for i in betweenness][:initial_outbreak_size]

<<<<<<< HEAD:abm_network/model.py
=======
        return []
>>>>>>> 21342aa8d8bccb494fa8227c2f6698a343fc0ed7:SIROD/abm_network/model.py

    def resistant_susceptible_ratio(self):
        """
        Compute ration resistant / susceptible
        :return ratio: float
        """
        try:
            return number_state(self, State.RESISTANT) / number_state(
                self, State.SUSCEPTIBLE
            )
        except ZeroDivisionError:
            return math.inf


    def step(self):
        """
        Mesa model step
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        # print(regenerate_network(self.G, self.grid))


    def run_model(self, n):

        """
        Run model for fixed number of iteration
        :param n: number of simulation steps
        """
        
        for _ in range(n):
            self.step()

    def print_infected(self):
        """
        Prints infected nodes in matrix form
        """
        l1 = [j['agent'][0].state.value for (i,j) in self.G.nodes(data=True)]
        print(l1)
        self.matrix.append(l1)
        print(number_susceptible(self), number_infected(self), number_resistant(self))


