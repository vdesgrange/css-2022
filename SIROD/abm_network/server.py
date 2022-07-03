import math
from .model import AntivirusOnNetwork, VirusOnNetwork, State, number_death, number_infected, number_offline
from mesa.visualization.modules import NetworkModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from .constants import NODE_COLORMAP
from .parameters import functional_model_params

def network_portrayal(G):
    """
    Networt portrayal provides set of function used for visualization of the MESA NetworkGrid.
    The model ensures there is always 1 agent per node
    :param G: graph
    """
    def node_color(agent):
        """
        Get node color based on agent state
        :param agent
        """
        return NODE_COLORMAP.get(agent.state, NODE_COLORMAP["Default"])

    def edge_color(agent1, agent2):
        """
        Get edge color based on agent state
        :param agent1: source agent
        :param agent2: target agent
        """
        if State.DEATH in (agent1.state, agent2.state):
            return "FFFFFFF"
        if State.OFFLINE in (agent1.state, agent2.state):
            return "#FFFFFF"
        if State.RESISTANT in (agent1.state, agent2.state): 
            return "#F4F9F9"
        return "#e8e8e8"

    def edge_width(agent1, agent2):
        """
        Get edge width based on agent state
        :param agent1: source agent
        :param agent2: target agent
        """
        if State.RESISTANT in (agent1.state, agent2.state):
            return 2
        return 2.5

    def get_agents(source, target):
        """ Get agents per source and target """
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 3 + agents[0].importance * 5,
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

# Phase charts
phase_chart = ChartModule(
    [
        {"Label": "Infected", "Color": "#FF0000"},
        {"Label": "Susceptible", "Color": "#008000"},
        {"Label": "Resistant", "Color": "#808080"},
        {"Label": "Offline", "Color": "#000000"},
        {"Label": "Death", "Color": "#FFC0CB"}
    ]
)

# Number of clusters in network charts
cluster_chart = ChartModule(
    [
        {"Label": "Clusters", "Color": "#000000"},
    ]
)

# Network cluster coefficient charts
cluster_coeff = ChartModule(
    [

        {"Label": "Ccoeff", "Color": "#000000"},
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


# Launch server
server = ModularServer(
    AntivirusOnNetwork,
    [network,
     get_resistant_susceptible_ratio,
     phase_chart,
     cluster_chart,
     cluster_coeff],
    "Malware propagation in complex networks",
    functional_model_params,
)
server.port = 8521
