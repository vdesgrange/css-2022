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
To solve this issue, install mesa (from source) into the code base directory:

```
git clone git@github.com:projectmesa/mesa.git
```

Once cloned, go to folder and run

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

## Architecture

- agents.py - Mesa malware agent class
- analysis.py - Functions used to aggregate model data for further analysis
- constants.py - Constants used in the model
- model.py - Mesa model class
- parameters.py - Parameters used by Mesa server
- rule_functions.py - Functions to be used for model/agent probabilities
- server.py - Mesa server
- simulations.py - Example of script for model simulation analysis
