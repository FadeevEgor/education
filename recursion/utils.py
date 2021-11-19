from itertools import combinations
from random import shuffle

import networkx as nx
from matplotlib import pyplot as plt
import pandas as pd

from pathfinder import PathFinder as PF


def get_setup(size):
    nodes = range(size)
    possible_edges = list(combinations(nodes, 2))
    shuffle(possible_edges)

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    while not nx.is_connected(graph):
        graph.add_edge(*possible_edges.pop())
    return graph, possible_edges


def calls_vs_connectivity(graph, possible_edges):
    nodes = graph.number_of_nodes()
    edges, calls, success = [], [], []


    while True:
        pf = PF(graph)
        path = pf.find_path()
        succ = (path is not None)
        calls.append(pf.calls)
        edges.append(graph.number_of_edges())
        success.append(succ)
        if not possible_edges:
            break
        graph.add_edge(*possible_edges.pop())

    df = pd.DataFrame(
        data={
            "edges": edges,
            "calls": calls,
            "success": success
        }
    )
    df["nodes"] = nodes
    return df


def plot_path(path, save_to=None):
    path_edges = [(path[i], path[i + 1], i/len(path)) for i in range(len(path) - 1)]
    path_graph = nx.DiGraph()
    path_graph.add_weighted_edges_from(path_edges)
    fig, ax = plt.subplots()

    pos = nx.shell_layout(path_graph)
    starting_node = path[0]
    x, y = pos[starting_node]
    ax.scatter([x], [y], color="r", s=1000)
    nx.draw(path_graph, pos=pos, with_labels=True, font_weight='bold', ax=ax)
    ax.set_title(" -> ".join([str(p) for p in path]))
    if save_to is None:
        plt.show()
    else:
        plt.savefig(save_to)


