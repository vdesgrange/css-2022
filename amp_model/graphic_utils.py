import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from networkx.drawing.nx_agraph import graphviz_layout
from constants import COLORMAP, NUM_COLORS
from matplotlib import animation, rc
from IPython.display import HTML


def get_edge_colormap(network, inf, sup):
    cm = plt.cm.Blues
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])


def show_state(states_over_time, name):
    """
    Simple visualization tool of the graph
    """
    num_time_steps = len(states_over_time)

    # Create graph
    G = states_over_time[0][0]
    L = states_over_time[0][1]
    pos = graphviz_layout(G, prog="twopi", args="")
    # set-up figure
    fig, ax = plt.subplots(figsize=(8, 8))
    # im = plt.imshow(states_over_time[0], animated=True)
    # plt.set_cmap('Greys')

    def update(i):
        ax.clear()
        G = states_over_time[i][0]
        L = states_over_time[i][1]
        cm = plt.cm.Reds_r
        gr = plt.cm.Greys

        node_color = [gr(L[id] / max(L)) for id in list(G.nodes)]
        edge_color = [cm(1. * G.edges[it[0], it[1]]['flow'] / NUM_COLORS) for it in list(G.edges)]

        nx.draw_networkx_edges(G, pos, edgelist=list(G.edges), edge_color=edge_color, edge_vmin=0., edge_vmax=1.)
        nx.draw_networkx_nodes(G, pos,
        nodelist=list(G.nodes),
        node_color=node_color,
        node_size=300,
        alpha=0.7)

        ax.set_title("Frame %d"%(i+1), fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, update, frames=num_time_steps, interval=200)
    anim.save(name)
    return HTML(anim.to_html5_video())


def visualize(G):
    """
    Simple visualization tool of the graph
    """
    pos = graphviz_layout(G, prog="twopi", args="")
    cm = plt.cm.Reds_r

    node_color = [COLORMAP[G.nodes[id]['bus_type']] for id in list(G.nodes)]
    edge_color = [cm(1. * G.edges[it[0], it[1]]['flow'] / NUM_COLORS) for it in list(G.edges)]

    plt.figure(figsize=(8, 8))

    nx.draw_networkx_edges(G, pos, edgelist=list(G.edges), edge_color=edge_color, alpha=0.4, width=3)
    nx.draw_networkx_nodes(G, pos,
                       nodelist=list(G.nodes),
                       node_color=node_color,
                       node_size=1000,
                       alpha=0.7)

    plt.axis("equal")
    plt.show()


def plot_average_efficiency(xs, alphas):
    """
    Plot averange efficiency of the network
    :param x: average efficiency per timesteps
    :param alpha: alpha used in simulation
    """
    fig, ax = plt.subplots()

    for idx, x in enumerate(xs):
        y = range(0, len(x))
        ax.plot(y, x, label=r'$\alpha$ = {:}'.format(alphas[idx]))

    ax.set_title("Efficiency E of the network per time")
    ax.set_xlabel("time")
    ax.set_ylabel("E")

    plt.legend()
    plt.show()
