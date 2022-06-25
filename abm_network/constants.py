from enum import Enum

class State(int, Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RESISTANT = 2
    OFFLINE = 3
    DEATH = 4


NODE_COLORMAP = {
    State.DEATH: "#FFC0CB", 
    State.OFFLINE: "#000000", 
    State.INFECTED: "#FF0000", 
    State.SUSCEPTIBLE: "#008000",
    "Default": "#808080"
}
