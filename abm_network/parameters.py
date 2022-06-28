from mesa.visualization.UserParam import Slider, Choice
from .rule_functions import *

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

functional_model_params = {
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
    "malware_spread_chance": malware_spread_chance,
    "malware_check_frequency":  malware_check_frequency,
    "recovery_chance":  recovery_chance,
    "gain_resistance_chance":  gain_resistance_chance,
    "susceptible_chance":  susceptible_chance,
    "death_chance":  death_chance,
    "importance": importance_degree,
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

analysis_params_a = {
    "num_nodes": [10, 100, 1000],
    "avg_node_degree": 3,
    "initial_outbreak_size": 1,
    "malware_spread_chance": malware_spread_chance,
    "malware_check_frequency":  malware_check_frequency,
    "recovery_chance":  recovery_chance,
    "gain_resistance_chance":  gain_resistance_chance,
    "susceptible_chance":  susceptible_chance,
    "death_chance":  death_chance,
    "centrality": "closeness",
    "network": "Erdos-Renyi"
}

cluster_analysis_params = {
    "num_nodes": 50,
    "avg_node_degree": 3,
    "initial_outbreak_size": 3,
    "centrality": "last",
    "malware_spread_chance": malware_spread_chance,
    "malware_check_frequency":  malware_check_frequency,
    "recovery_chance":  recovery_chance,
    "gain_resistance_chance":  gain_resistance_chance,
    "importance": importance_degree,
    "network": "Barabasi-Albert",
    "matrix": [],
    "susceptible_chance":  susceptible_chance,
    "death_chance":  death_chance,
}
