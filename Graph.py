from conversions import *


class Graph:
    adjacencyMatrix = None
    adjacencyList = None
    incidenceMatrix = None

    def __init__(self, file_path=None, graph_representation="a_m", info=True):
        if file_path is None:
            self.data = [[None]]
            self.represent = "a_m"
        else:
            with open(file_path, 'r') as f:
                data = [[int(val) if '0' not in val else 0 for val in line.split(' ')] if line != '\n' else [] for
                        line in f]
            self.data = data
            self.represent = graph_representation

        if info is True:
                print("Graph represented by " +
                      ("adjacency matrix." if self.represent == "a_m"
                       else ("incidence matrix." if self.represent == "i_m"
                             else "adjacency list.")))
        if self.represent == "a_m":
            self.adjacencyMatrix = self.data
            self.adjacencyList = adj_matrix_to_adj_list(self.adjacencyMatrix)
            self.incidenceMatrix = adj_matrix_to_inc_matrix(self.adjacencyMatrix)
        elif self.represent == "i_m":
            self.incidenceMatrix = self.data
            self.adjacencyMatrix = inc_matrix_to_adj_matrix(self.incidenceMatrix)
            self.adjacencyList = inc_matrix_to_adj_list(self.incidenceMatrix)
        else:
            self.adjacencyList = self.data
            self.adjacencyMatrix = adj_list_to_adj_matrix(self.adjacencyList)
            self.incidenceMatrix = adj_list_to_inc_matrix(self.adjacencyList)

    def __str__(self):
        return str(self.print_all_representations())

    def print_all_representations(self):
        print(self.adjacencyList)
        print(self.adjacencyMatrix)
        print(self.incidenceMatrix)
