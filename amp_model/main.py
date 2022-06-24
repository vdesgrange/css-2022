import numpy as np
from networks import Barabasi_Albert_Network
from graphic_utils import visualize 
from model import amp_model

def experiment_1():
    """
    Different alpha for small barabasi-albert graph
    :return:
    """
    bara = Barabasi_Albert_Network(20, 5, 1.01)
    visualize(bara.G)
    bara.set_edges('flow', 1)
    amp_model(bara, 50, [0])


if __name__ == '__main__':
    experiment_1()
