import numpy as np
from networks import Barabasi_Albert_Network
from graphic_utils import visualize, show_state
from model import amp_model

def experiment_1():
    """
    Different alpha for small barabasi-albert graph
    :return:
    """
    bara = Barabasi_Albert_Network(100, 5, 0.01)
    visualize(bara.G)
    bara.set_edges('flow', 1)
    s = amp_model(bara, 50, [0])
    show_state(s, 'example.gif')


if __name__ == '__main__':
    experiment_1()
