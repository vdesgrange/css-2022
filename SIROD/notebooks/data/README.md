# Data used in analysis
## Study of cluster distribution

### cluster_distribution_1.p

100 nodes
Barabasi-Albert
Barabasi-Albert
```
cluster_analysis_params = {
    "num_nodes": 100, # 100
    "avg_node_degree": 3, # 3
    "initial_outbreak_size": 1, # 1
    "centrality": "degree", # degree
    "malware_spread_chance": 0.4, # 0.4
    "malware_check_frequency":  0.4,  # 0.4[, 0.1, 0.8]
    "recovery_chance":  0.4,
    "gain_resistance_chance": gain_resistance_chance,
    "importance": importance_degree,
    "susceptible_chance":  susceptible_chance,
    "death_chance":  death_chance,
    "network": "Barabasi-Albert",
}

n_run = 100
results = mesa.batch_run(
    VirusOnNetwork,
    parameters=cluster_analysis_params,
    iterations=n_run,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)
```

### cluster_distribution_2.p (not included)

1000 nodes
Barabasi-Albert

```
cluster_analysis_params = {
    "num_nodes": 1000,
    "avg_node_degree": 3,
    "initial_outbreak_size": 1,
    "centrality": "degree",
    "malware_spread_chance": 0.4,
    "malware_check_frequency":  0.4,
    "recovery_chance":  0.4,
    "gain_resistance_chance": gain_resistance_chance,
    "importance": importance_degree,
    "susceptible_chance":  susceptible_chance,
    "death_chance":  death_chance,
    "network": "Barabasi-Albert",
}

n_run = 100
results = mesa.batch_run(
    VirusOnNetwork,
    parameters=cluster_analysis_params,
    iterations=n_run,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)
```

### cluster_distribution_3.p

100 nodes
Erdos-Renyi

```
cluster_analysis_params = {
    "num_nodes": 100,
    "avg_node_degree": 3,
    "initial_outbreak_size": 1,
    "centrality": "degree",
    "malware_spread_chance": 0.4,
    "malware_check_frequency":  0.4,
    "recovery_chance":  0.4,
    "gain_resistance_chance": gain_resistance_chance,
    "importance": importance_degree,
    "susceptible_chance":  susceptible_chance,
    "death_chance":  death_chance,
    "network": "Erdos-Renyi",
}

n_run = 100
results = mesa.batch_run(
    VirusOnNetwork,
    parameters=cluster_analysis_params,
    iterations=n_run,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)
```
