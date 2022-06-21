
"""
([reference] Advance malware propagation on random complex network)
Coefficients of the model - table 1
"""
COEFF = {
    "H": 0.25,
    "A": 0.1,
    "B": 0.5,
    "D": 0.4,
    "Rs": 0.4,
    "T": 4,
    "Tau": 12
}

STATES = {
    "S": 0,
    "I": 1,
    "A": 2,
    "R": 3
}

COLORMAP = dict([('S', 'yellow'), ('I','orange'), ('A', 'red'), ('R', 'blue')])
