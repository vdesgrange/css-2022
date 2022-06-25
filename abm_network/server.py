import math
from .model import VirusOnNetwork, State, number_death, number_infected, number_offline
from mesa.visualization.modules import NetworkModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, Choice
from .constants import NODE_COLORMAP

def network_portrayal(G):
    # The model ensures there is always 1 agent per node

    def node_color(agent):
        return NODE_COLORMAP.get(agent.state, NODE_COLORMAP["Default"])

    def edge_color(agent1, agent2):
        if State.DEATH in (agent1.state, agent2.state):
            return "FFFFFFF"
        if State.RESISTANT in (agent1.state, agent2.state) or State.OFFLINE in (agent1.state, agent2.state):
            return "#FFFFFF"
        return "#e8e8e8"

    def edge_width(agent1, agent2):
        if State.RESISTANT in (agent1.state, agent2.state):
            return 3
        return 2

    def get_agents(source, target):
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": f"id: {agents[0].unique_id}<br>state: {agents[0].state.name}",
        }
        for (_, agents) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": edge_color(*get_agents(source, target)),
            "width": edge_width(*get_agents(source, target)),
        }
        for (source, target) in G.edges
    ]

    return portrayal


network = NetworkModule(network_portrayal, 1000, 1000)

phase_chart = ChartModule(
    [
        {"Label": "Infected", "Color": "#FF0000"},
        {"Label": "Susceptible", "Color": "#008000"},
        {"Label": "Resistant", "Color": "#808080"},
        {"Label": "Offline", "Color": "#000000"},
        {"Label": "Death", "Color": "#FFC0CB"}
    ]
)

cluster_chart = ChartModule(
    [

        {"Label": "Clusters", "Color": "#000000"},
    ]
)

def get_resistant_susceptible_ratio(model):
    ratio = model.resistant_susceptible_ratio()
    ratio_text = "&infin;" if ratio is math.inf else f"{ratio:.2f}"
    infected_text = str(number_infected(model))
    offline_text = str(number_offline(model))
    death_text = str(number_death(model))

    return "Resistant/Susceptible Ratio: {}<br>Infected Remaining: {}<br>Offline: {}<br>Death: {}".format(
        ratio_text, infected_text, offline_text, death_text
    )


model_params = {
    "num_nodes":  Slider(
        "Number of agents",
        10,
        10,
        500,
        1,
        description="Choose how many agents to include in the model",
    ),
    "avg_node_degree":  Slider(
        "Avg Node Degree", 3, 3, 8, 1, description="Avg Node Degree"
    ),
    "initial_outbreak_size":  Slider(
        "Initial Outbreak Size",
        1,
        1,
        10,
        1,
        description="Initial Outbreak Size",
    ),
    "malware_spread_chance":  Slider(
        "Virus Spread Chance",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Probability that susceptible neighbor will be infected",
    ),
    "malware_check_frequency":  Slider(
        "Virus Check Frequency",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Frequency the nodes check whether they are infected by " "a virus",
    ),
    "recovery_chance":  Slider(
        "Recovery Chance",
        0.3,
        0.0,
        1.0,
        0.1,
        description="Probability that the virus will be removed",
    ),
    "gain_resistance_chance":  Slider(
        "Gain Resistance Chance",
        0.5,
        0.0,
        1.0,
        0.1,
        description="Probability that a recovered agent will become "
        "resistant to this virus in the future",
    ),
    "centrality": Choice(
        "Infected Node Centrality",
        'random',
        ['random', 'degree', 'closeness', 'betweenness'],
        description="First infected node(s) are based on centrality"
    ),
    "network": Choice(
        "Network Topology",
        'Erdos-Renyi',
        ['Erdos-Renyi', 'Watts-Strogatz', 'Barabasi-Albert'],
        description="Network Types (Random, Small-World, Scale Free)"
    )
}

server = ModularServer(
    VirusOnNetwork,
    [network, 
     get_resistant_susceptible_ratio, 
     phase_chart,
     cluster_chart],
    "Malware propagation in complex networks",
    model_params,
)
server.port = 8521
