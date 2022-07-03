# Malware propagation through network

## Description

Implementation based on the papers:
- Advanced malware propagation on random complex networks (Del Rey et al. 2020)
- A New Individual-Based Model to Simulate Malware Propagation in Wireless Sensor Networks


Extra features implemented on ABM model based on networkX:
- Different network topologies (ER, WS, BA)
- Select infected node(s) based on centrality (degree, closeness, betweenness, random)
- Probabilities to be determined from constants (default) or functions.
- Print states of every node per timestep in matrix for lattice
- Implemented offline nodes, death nodes

### Installation

mesa library provided by package manager (pip, conda) might not run.
To solve this issue, install the git submodule from the root of this repository

```
git submodule init
git submodule update
```

Or directly install mesa (from source) into the code base directory `SIROD/abm_network/` :

```
git clone git@github.com:projectmesa/mesa.git
```

Once cloned, go to `SIROD/abm_network/mesa` folder and run

```
sudo python setup.py install
```

### Run Model

To run the model, run in terminal

```
python3 run.py
```

Now go to

http://127.0.0.1:8521/

#### How to experiment with different models or parameters ?
Go into `./abm_network/server.py`

Choose `VirusOnNetwork` (default model based on malware spread using S-I-R-O-D compartment rules) or `AntivirusOnNetwork` (model using antivirus agent) from `model.py` file.

Choose set of parameters from `parameters.py` file.

```
server = ModularServer(
    VirusOnNetwork, # Model
    [network,
     get_resistant_susceptible_ratio,
     phase_chart,
     cluster_chart,
     cluster_coeff],
    "Malware propagation in complex networks",
    functional_model_params, # parameters
)
```


## Architecture

- run.py - Run simulation interface
- run_experiments.py - A file used to generate some of simulation data for analysis.
- abm_network/ - source code
    - agents.py - Mesa malware (main agent) and antivirus agent classes
    - analysis.py - Functions used to aggregate model data for further analysis
    - constants.py - Constants used in the model
    - model.py - Mesa VirusOnNewtwork (main model) and AntivirusOnNetwork model classes.
    - parameters.py - Parameters used by Mesa server
    - rule_functions.py - Functions to be used for model/agent probabilities
    - server.py - Mesa server.
    - simulations.py - Example of script for model simulation analysis
- notebooks/ - Contains jupyter notebooks used for analysis of simulation data.
    - notebooks/data - Contains data generated through multiple simulation, used for analysis
- cluster_distribution_analysis.ipynb - Jupyter notebook for cluster analysis. Not located in notebooks directory due to direct import of abm_network package source code.
