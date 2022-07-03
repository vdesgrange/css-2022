import math
import random
import networkx as nx
import mesa
from mesa.model import Model
from .constants import State
from .agents import MalwareAgent
from .analysis import regenerate_network, get_clusters, get_clustering_coefficient
counter = 0
flag = False


def number_state(model, state):
    return sum(1 for a in model.grid.get_all_cell_contents() if a.state is state)


def number_infected(model):
    return number_state(model, State.INFECTED)


def number_susceptible(model):
    return number_state(model, State.SUSCEPTIBLE)


def number_resistant(model):
    return number_state(model, State.RESISTANT)


def number_offline(model):
    return number_state(model, State.OFFLINE)


def number_death(model):
    return number_state(model, State.DEATH)


def number_clusters(model):
    H = regenerate_network(model.G, model.grid)
    return get_clusters(H)


def clustering_coeff(model):
    H = regenerate_network(model.G, model.grid)
    return get_clustering_coefficient(H)


class VirusOnNetwork(Model):

    """A malware model with some number of agents"""

    def __init__(
        self,
        num_nodes=30,
        avg_node_degree=3,
        initial_outbreak_size=2,
        centrality="random",
        malware_spread_chance=0.4,
        malware_check_frequency=0.2,
        recovery_chance=0.3,
        gain_resistance_chance=0.5,
        network="erdos-renyi",
        matrix = [],
        importance = random.uniform(0, 1),
        susceptible_chance = 0.1,
        death_chance = 0.00,
        antivirus = False,
    ):

        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = self.get_network(network, prob)
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
        self.antivirus = antivirus

        self.datacollector = mesa.DataCollector(
            {
                "Infected": number_infected,
                "Susceptible": number_susceptible,
                "Resistant": number_resistant,
                "Offline": number_offline,
                "Death": number_death,
                "Clusters": number_clusters,
                "Ccoeff": clustering_coeff,
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
                self.importance,
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

        # self.print_infected()
        # print([j['agent'][0].state.value for (i,j) in self.G.nodes(data=True)])


    def get_network(self, network, prob):
        if network.lower() == "erdos-renyi":
            return nx.erdos_renyi_graph(n = self.num_nodes, p = prob, seed = 22)

        elif network.lower() == "barabasi-albert":
            return nx.barabasi_albert_graph(n = self.num_nodes, m = 1, seed = 22)

        else:
            return nx.watts_strogatz_graph(n = self.num_nodes, k = int(0.2*(self.num_nodes)), p = prob, seed = 22)


    def set_initial_outbreak(self, initial_outbreak_size, centrality = "random", descending = True):
        
        """
        Set initial outbreak nodes
        centralities:
        - None (random)
        - degree centrality
        - Closeness
        - Betweennes
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


    def resistant_susceptible_ratio(self):

        try:
            return number_state(self, State.RESISTANT) / number_state(
                self, State.SUSCEPTIBLE
            )
        except ZeroDivisionError:
            return math.inf

    def resistant_susceptible__infected_ratio(self):

        try:
            return number_state(self, State.RESISTANT) / number_state(
                self, State.SUSCEPTIBLE
            )
        except ZeroDivisionError:
            return math.inf


    def offline_infected_susceptible_ratio(self):

        """ Ratio offline nodes vs susceptible + infected nodes """

        try:
            return (number_state(self, State.OFFLINE)) / (number_state(
                self, State.SUSCEPTIBLE
            ) + number_state(self, State.INFECTED))
        except ZeroDivisionError:
            return math.inf

    
    def try_create_antivirus(self):

        if random.random() < 0.05: self.antivirus = True

        elif self.offline_infected_susceptible_ratio() > 0.6:
            self.antivirus = True


    def step(self):

        global counter
        global flag
        counter += 1
        self.schedule.step()
        row = [j['agent'][0].state.value for (i,j) in self.G.nodes(data=True)]
        # self.matrix.append(row)
        # collect data
        self.datacollector.collect(self)
        self.try_create_antivirus()

        if self.antivirus and not flag:
            print(f"Antivirus found at step {counter}, nw size = {self.num_nodes}")
            flag = True
        # print(self.antivirus)

    def run_model(self, n):

        for i in range(n):
            self.step()


    def print_infected(self):

        """ prints infected nodes in matrix form """

        # l1 = [j['agent'][0].state.value for (i,j) in self.G.nodes(data=True)]
        # print(l1)
        # self.matrix.append(l1)
        print(number_susceptible(self), number_infected(self), number_resistant(self))