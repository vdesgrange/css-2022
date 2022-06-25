# Complex Systems Simulation 2022
Malware propagation through network
Basic implementation based on the papers:
Advanced malware propagation on random complex networks (Del Rey et al. 2020)
A New Individual-Based Model to Simulate Malware Propagation in Wireless Sensor Networks


Extra features implemented on ABM model based on networkX:
- Different network topologies (ER, WS, BA)
- Select infected node(s) based on centrality (degree, closeness, betweenness, random)
- Print states of every node per timestep in matrix for lattice
- Implemented offline nodes, Death nodes


install mesa (from source)

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
