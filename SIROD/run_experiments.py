from abm_network.simulations import simulations, simulate_barabasi_albert

# get

max_spread = []

for i in range(100):
    max_spread.append(simulate_barabasi_albert())

avg = sum(max_spread)/len(max_spread)
print(f"Average spread is {avg}")
