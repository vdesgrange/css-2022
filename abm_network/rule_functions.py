import numpy as np

def malware_spread_chance(model):
    return 0.4

def malware_check_frequency(model):
    return 0.4

def recovery_chance(model):
    return 0.3

def gain_resistance_chance(model):
    return 0.5

def importance():
    return np.random.beta(5, 5)

def importance_degree():
    rand = np.random.beta(5, 5)
    f = lambda a : 0.6 * rand + 0.4 * (a.model.G.degree[a.unique_id] / a.model.k_max)
    return f


def susceptible_chance(model):
    return 0.01

def death_chance(model):
    return 0.01
