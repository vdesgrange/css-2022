from enum import Enum

class State(int, Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RESISTANT = 2
    OFFLINE = 3
    DEATH = 4
