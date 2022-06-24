import numpy as np
from networks import Barabasi_Albert_Network
from graphic_utils import visualize, show_state
from model import amp_model
from analysis import time_analysis

def experiment_1():
    """
    Different alpha for small barabasi-albert graph
    :return:
    """
    bara = Barabasi_Albert_Network(50, 5, 0.02)
    s = amp_model(bara, 50, [0])
    show_state(s, 'example.gif')
    time_analysis(s)


if __name__ == '__main__':
    experiment_1()
