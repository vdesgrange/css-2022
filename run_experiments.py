from abm_network.simulations import simulations, simulations_until_resistant
ts = []

for i in range(100):

    x = simulations_until_resistant()
    ts.append(x)

print(ts)