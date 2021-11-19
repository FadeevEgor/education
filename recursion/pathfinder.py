import numpy as np
import networkx as nx

class PathFinder:
    def __init__(self, graph):
        self.graph = graph
        self.n_nodes = graph.number_of_nodes()
        self.adjacency_matrix = nx.adjacency_matrix(graph).todense()
        self.edges_visited = np.zeros(shape=(self.n_nodes, self.n_nodes), dtype=bool)
        self.path = []
        self.success = False
        self.calls = 0

    def find_path(self):
        self.calls = 0
        self.success = False
        for i in range(self.n_nodes):
            self.path = [i]
            succ, path = self.__find_path_rec(i)
            if succ:
                return path
        return None

    def __mark_visited(self, i, j):
        self.path.append(j)
        self.edges_visited[i, j] = True
        self.edges_visited[j, i] = True

    def __unmark(self, i, j):
        self.path.pop()
        self.edges_visited[i, j] = False
        self.edges_visited[j, i] = False

    def __check(self):
        return np.array_equal(self.adjacency_matrix, self.edges_visited)

    def __find_path_rec(self, i):
        self.calls += 1
        success = self.__check()
        if success:
            return True, self.path.copy()

        for j in self.graph.neighbors(i):
            if not self.edges_visited[i, j]:
                self.__mark_visited(i, j)
                succ, path = self.__find_path_rec(j)
                if succ:
                    return True, path
                self.__unmark(i, j)

        return False, None
