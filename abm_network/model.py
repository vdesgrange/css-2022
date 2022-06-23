import math
from enum import Enum
import networkx as nx
import mesa
from mesa.model import Model
from mesa.agent import Agent
import random


class State(Enum):

    SUSCEPTIBLE = 0
    INFECTED = 1
    RESISTANT = 2
    OFFLINE = 3

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


class VirusOnNetwork(Model):

    """A malware model with some number of agents"""

    def __init__(
        self,
        num_nodes=30,
        avg_node_degree=3,
        initial_outbreak_size=2,
        centrality="random",
        malware_spread_chance=0.4,
        malware_check_frequency=0.4,
        recovery_chance=0.3,
        gain_resistance_chance=0.5,
        network="erdos-renyi",
        matrix = [],
        importance = random.uniform(0, 1),
        susceptible_chance = 0.1
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

        self.datacollector = mesa.DataCollector(
            {
                "Infected": number_infected,
                "Susceptible": number_susceptible,
                "Resistant": number_resistant,
                "Offline": number_offline,
            }
        )

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            a = malwareAgent(
                i,
                self,
                State.SUSCEPTIBLE,
                self.malware_spread_chance,
                self.malware_check_frequency,
                self.recovery_chance,
                self.gain_resistance_chance,
                self.importance,
                self.susceptible_chance
            )
            self.schedule.add(a)
            # Add the agent to the node
            self.grid.place_agent(a, node)

        # Infect some nodes
        infected_nodes = self.set_initial_outbreak(initial_outbreak_size, centrality, descending = True)

        for a in self.grid.get_cell_list_contents(infected_nodes):
            a.state = State.INFECTED

        self.running = True
        self.datacollector.collect(self)

        # self.print_infected()
        print([j['agent'][0].state.value for (i,j) in self.G.nodes(data=True)])


    def get_network(self, network, prob):
        if network.lower() == "erdos-renyi":
            return nx.erdos_renyi_graph(n = self.num_nodes, p = prob)

        elif network.lower() == "barabasi-albert":
            return nx.barabasi_albert_graph(n = self.num_nodes, m = 1)

        else:
            return nx.watts_strogatz_graph(n = self.num_nodes, k = int(0.2*(self.num_nodes)), p = prob, seed = None)


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

    def step(self):
        self.schedule.step()
        row = [j['agent'][0].state.value for (i,j) in self.G.nodes(data=True)]
        self.matrix.append(row)
        # collect data
        self.datacollector.collect(self)
        print(self.matrix)

    def run_model(self, n):

        for i in range(n):
            self.step()

    def print_infected(self):
        l1 = [j['agent'][0].state.value for (i,j) in self.G.nodes(data=True)]
        print(l1)
        self.matrix.append(l1)
        print(number_susceptible(self), number_infected(self), number_resistant(self))


class malwareAgent(Agent):

    def __init__(
        self,
        unique_id,
        model,
        initial_state,
        malware_spread_chance,
        malware_check_frequency,
        recovery_chance,
        gain_resistance_chance,
        importance,
        susceptible_chance,
    ):
        super().__init__(unique_id, model)

        self.state = initial_state
        self.malware_spread_chance = malware_spread_chance
        self.malware_check_frequency = malware_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance
        self.importance = importance
        self.susceptible_chance = susceptible_chance


    def try_to_notify_neighbors(self):

        """ if importance under 0.8, nodes can shut themselves down in order to prevent being infected """

        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]

        for a in susceptible_neighbors:
            if a.importance < 0.8:
                offline_probability = 1 - a.importance
            if self.random.random() < offline_probability:
                a.state = State.OFFLINE

    def try_to_infect_neighbors(self):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]
        for a in susceptible_neighbors:
            if self.random.random() < self.malware_spread_chance:
                a.state = State.INFECTED


    def try_be_susceptible(self):
        if self.random.random() < self.susceptible_chance:
            self.state = State.SUSCEPTIBLE

    def try_to_reboot(self):
        if self.random.random() < self.importance:
            self.state = State.SUSCEPTIBLE

    def try_gain_resistance(self):
        if self.random.random() < self.gain_resistance_chance:
            self.state = State.RESISTANT

    def try_remove_infection(self):
        # Try to remove
        if self.random.random() < self.recovery_chance:
            # Success
            self.state = State.SUSCEPTIBLE
            self.try_gain_resistance()
        else:
            # Failed
            self.state = State.INFECTED

    def try_check_situation(self):
        if self.random.random() < self.malware_check_frequency:
            # Checking...
            if self.state is State.INFECTED:
                self.try_remove_infection()
            if self.state is State.OFFLINE:
                self.try_to_reboot()
            if self.state is State.RESISTANT:
                self.try_be_susceptible()

    def step(self):
        if self.state is State.INFECTED:
            self.try_to_infect_neighbors()
            self.try_to_notify_neighbors()
        self.try_check_situation()
