from itertools import combinations
from random import shuffle
import os

import networkx as nx
from matplotlib import pyplot as plt
import pandas as pd
from matplotlib import cm

from routefinder import RouteFinder as RF
from tqdm import tqdm

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
    edges, calls, routes, calls_total = [], [], [], []

    bar = tqdm(total=len(possible_edges))
    while True:
        rf = RF(graph)
        rf.find_route()
        calls.append(rf.calls)
        edges.append(graph.number_of_edges())
        rf.find_all_routes()
        routes.append(len(rf.routes))
        calls_total.append(rf.calls)
        if not possible_edges:
            break
        graph.add_edge(*possible_edges.pop())
        bar.update()

    df = pd.DataFrame(
        data={
            "edges": edges,
            "calls": calls,
            "routes": routes,
            "calls_total": calls
        }
    )
    df["nodes"] = nodes
    bar.close()
    return df


def plot_all_routes(graph, possible_edges, folder="./pictures/"):
    plt.rc('text', usetex=True)
    plt.rc('font', size=24)
    plt.rcParams['text.latex.preamble'] = r"""
    \usepackage[utf8]{inputenc}
    \usepackage[english,russian]{babel}
    \usepackage{amsmath}
    """
    nodes = graph.number_of_nodes()
    folder_to_save = os.path.join(folder, f"{nodes}_nodes")
    os.makedirs(folder_to_save, exist_ok=True)
    bar = tqdm(total=len(possible_edges))
    while True:
        pf = RF(graph)
        routes = pf.find_all_routes()
        for i, route in enumerate(routes):
            filename = f"{graph.number_of_edges()}_edges_{i:04}.png"
            path_to_save = os.path.join(folder_to_save, filename)
            plot_route(graph, route, path_to_save)
        if not possible_edges:
            break
        bar.update()
        graph.add_edge(*possible_edges.pop())


def plot_route(graph, route, save_to=None):
    route_edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
    str_route = r"\to".join([str(r) for r in route])
    route_graph = nx.DiGraph()
    route_graph.add_edges_from(route_edges)
    edge_color = [i for i, _ in enumerate(route_edges)]
    pos = nx.layout.shell_layout(graph)
    kwargs = {
        "with_labels": True,
        "node_size": 700,
        "node_color": "lightskyblue",
        "font_size": 24,
        "font_weight": 'bold',
        "pos": pos
    }

    fig, axs = plt.subplots(ncols=2, figsize=(10, 5))
    fig.suptitle(f"${str_route}$", fontsize=24)
    nx.draw(graph, ax=axs[0], **kwargs)
    kwargs.update(edge_cmap=cm.get_cmap("jet"), edge_color=edge_color)
    nx.draw(route_graph, ax=axs[1], **kwargs)

    if save_to is None:
        plt.show()
    else:
        plt.savefig(save_to)
    plt.close(fig)
    fig.clear()
    for ax in axs:
        ax.clear()





