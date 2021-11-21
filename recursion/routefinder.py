import numpy as np
import networkx as nx

class RouteFinder:
    def __init__(self, graph):
        self.graph = graph
        self.n_nodes = graph.number_of_nodes()
        self.adjacency_matrix = nx.adjacency_matrix(graph).todense()
        self.edges_visited = np.zeros(shape=(self.n_nodes, self.n_nodes), dtype=bool)
        self.route = []
        self.routes = []
        self.success = False
        self.calls = 0

    def find_route(self):
        self.calls = 0
        self.success = False
        for i in range(self.n_nodes):
            self.route = [i]
            succ, route = self.__find_route_rec(i)
            if succ:
                return route
        return None

    def find_all_routes(self):
        self.calls = 0
        for i in range(self.n_nodes):
            self.route = [i]
            self.__find_all_routes_rec(i)
        return self.routes

    def __mark_visited(self, i, j):
        self.route.append(j)
        self.edges_visited[i, j] = True
        self.edges_visited[j, i] = True

    def __unmark_visited(self, i, j):
        self.route.pop()
        self.edges_visited[i, j] = False
        self.edges_visited[j, i] = False

    def __is_success(self):
        return np.array_equal(self.adjacency_matrix, self.edges_visited)

    def __find_route_rec(self, i):
        self.calls += 1
        success = self.__is_success()
        if success:
            return True, self.route.copy()

        for j in self.graph.neighbors(i):
            if not self.edges_visited[i, j]:
                self.__mark_visited(i, j)
                succ, route = self.__find_route_rec(j)
                if succ:
                    return True, route
                self.__unmark_visited(i, j)

        return False, None

    def __find_all_routes_rec(self, i):
        self.calls += 1
        success = self.__is_success()
        if success:
            self.routes.append(self.route.copy())
            self.success = True
            return

        for j in self.graph.neighbors(i):
            if not self.edges_visited[i, j]:
                self.__mark_visited(i, j)
                self.__find_all_routes_rec(j)
                self.__unmark_visited(i, j)

        return False, None
