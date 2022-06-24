from enum import Enum

"""
([reference] Advance malware propagation on random complex network)
Coefficients of the model - table 1
"""
class Coeff(float, Enum):
    H = 0.25,
    A = 0.1,
    B = 0.5,
    D = 0.4,
    Rs = 0.4,
    T = 4,
    Tau = 12

class State(int, Enum):
    S = 0,
    I = 1,
    A = 2,
    R = 3

COLORMAP = dict([(0, 'yellow'), (1,'orange'), (2, 'red'), (3, 'blue')])

NUM_COLORS = 20
