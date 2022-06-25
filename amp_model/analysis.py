import matplotlib.pyplot as plt
import numpy as np

def time_analysis(timeline):
    """
    Analyse the timeline of infected devices
    """
    healthy=[]
    exposed=[]
    infected=[]
    recovered=[]
    dead=[]

    for i in range(len(timeline)):
        G = timeline[i]
        temp = [G.nodes[id]['data'].state for id in list(G.nodes)]
        healthy.append(temp.count(0))
        exposed.append(temp.count(1))
        infected.append(temp.count(2))
        recovered.append(temp.count(3))
        dead.append(temp.count(4))

    x = np.linspace(0, len(timeline), len(timeline))
    plt.plot(x, healthy, 'o', color='blue')
    plt.plot(x, exposed, 'o', color='yellow')
    plt.plot(x, infected, 'o', color='red')
    plt.plot(x, recovered, 'o', color='green')
    plt.plot(x, dead, 'o', color='black')
    plt.show()

    return(healthy,exposed,recovered,infected,dead)


def detect_cluster(timeline):
    """
    Detect clusters
    """
    pass
