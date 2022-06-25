import random

def malware_spread_chance(model):
    return 0.4

def malware_check_frequency(model):
    return 0.4

def recovery_chance(model):
    return 0.3

def gain_resistance_chance(model):
    return 0.5

def importance(model):
    return random.uniform(0, 1)

def susceptible_chance(model):
    return 0.01

def death_chance(model):
    return 0.01
