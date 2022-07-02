import numpy as np

"""
rule_functions.py provide possibility to create functions which can be used in the ABM model.
ABM model check if parameter received are constants (default) or callable function (as provided here).
ie. Resistance variation per node based on a beta distribution.
Functions aims at providing more freedom in the rule coordinating the model.
"""
def importance():
    return np.random.beta(5, 5)

def importance_degree():
    """
    importance probability based on beta distribution and importance of the agent node.
    """
    rand = np.random.beta(5, 5)
    f = lambda a : 0.6 * rand + 0.4 * (a.model.G.degree[a.unique_id] / a.model.k_max)
    return f

def malware_spread_chance(model):
    return 0.4 # default

def malware_check_frequency(model):
    return 0.4 # default

def recovery_chance(model):
    return 0.3 # default

def gain_resistance_chance(model):
    return 0.5 # default

def susceptible_chance(model):
    return 0.01 # default

def death_chance(model):
    return 0.01 # default
