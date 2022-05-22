import numpy as np

from utils.conversions import *
import tkinter as tk
import math
import random
from utils.dijkstra import *
from utils.dfs import *

class Graph:
    adjacencyMatrix = None  # macierz sasiedztwa
    adjacencyList = None  # lista sasiedztwa
    incidenceMatrix = None  # macierz incydencji
    longest_comp = None  # najdłuższa spójna składowa
    weights = None  # wagi krawędzi
    minimumSpanningTree = None  # minimalne drzewo rozpinające jako adj_matrix
    adjacencyMatrixWeights = None #macierz sasiedztwa z wagami zamiast 1
    distanceMatrix = None #macierz odleglosci

    def __init__(self, file_path=None, graph_representation="a_m", weight_min= 1, weight_max = 10):
        if type(file_path) is str:
            if file_path is None:
                data = [[None]]
            else:
                with open(file_path, 'r') as f:
                    data = [[int(val) for val in line.split(' ')] if line != '\n' else [] for line in f]

            print("Graf reprezentowany jako: " + ("macierz sąsiedztwa." if graph_representation == "a_m"
                                             else (
                "macierz incydencji." if graph_representation == "i_m" else "lista sąsiedztwa.")))
        else:
            data = file_path

        if file_path is not None:
            if graph_representation == "a_m":
                self.adjacencyMatrix = np.copy(data)
                self.adjacencyMatrixWeights = self.adjacencyMatrix.copy()
                self.adjacencyList = adj_matrix_to_adj_list(self.adjacencyMatrix)
                self.incidenceMatrix = adj_matrix_to_inc_matrix(self.adjacencyMatrix)
            elif graph_representation == "i_m":
                self.incidenceMatrix = np.copy(data)
                self.adjacencyMatrix = inc_matrix_to_adj_matrix(self.incidenceMatrix)
                self.adjacencyList = inc_matrix_to_adj_list(self.incidenceMatrix)
                self.adjacencyMatrixWeights = self.adjacencyMatrix.copy()
            else:
                if type(file_path) is str:
                    key_values = list(range(1, len(data) + 1))
                    list_of_dict = defaultdict(list, dict(zip(key_values, data)))

                    self.adjacencyList = list_of_dict
                    self.adjacencyMatrix = adj_list_to_adj_matrix(self.adjacencyList)
                    self.incidenceMatrix = adj_list_to_inc_matrix(self.adjacencyList)
                    self.adjacencyMatrixWeights = self.adjacencyMatrix.copy()

                else:
                    self.adjacencyList = data
                    self.adjacencyMatrix = adj_list_to_adj_matrix(self.adjacencyList)
                    self.incidenceMatrix = adj_list_to_inc_matrix(self.adjacencyList)
                    self.adjacencyMatrixWeights = self.adjacencyMatrix.copy()

            self.longest_comp = self.components()
        if self.adjacencyList is not None:
            self.weights = self.weights_of_edges(weight_min, weight_max)
            self.init_weigth_matrix()
            self.distanceMatrix = self.generate_distance_matrix()

    def __str__(self):
        return str(self.print_all_representations())

    def print_all_representations(self):
        print("\nLista sąsiedztwa: \n")
        print(self.adjacencyList)
        print("\nMacierz sąsiedztwa: \n")
        print(self.adjacencyMatrix)
        print("\nMacierz incydencji: \n")
        print(self.incidenceMatrix)
        print(" ")

    def draw(self, title= "okno"):
        if self.adjacencyMatrix is None:
            print("Empty graph - cannot draw the graph.")
            return
        width = height = 800
        n = len(self.adjacencyMatrix)
        alfa = 2 * math.pi / n

        center_x = width / 2
        center_y = height / 2
        R = center_x * 3 / 4
        if n > 3:
            r = R / n
        else:
            r = R / n * 0.5

        window = tk.Tk()
        window.winfo_toplevel().title(title)
        window.geometry("800x800")
        canvas = tk.Canvas(window, height=height, width=width, bg="white")

        positions = []
        # set positions of vertices
        for i in range(n):
            positions.append([0.0, 0.0])
            if n > 1:
                positions[i][0] = center_y + R * math.sin(i * alfa)
                positions[i][1] = center_x - R * math.cos(i * alfa)
            else:
                positions[i][0] = center_x
                positions[i][1] = center_y
        canvas.create_oval(center_x - R, center_y - R, center_x + R, center_y + R, outline="blue", width=3, dash=(5, 1))
        # draw edges
        for i in range(1, n):
            for j in range(0, i):
                if self.adjacencyMatrix[i][j] == 1:
                    canvas.create_line(
                        positions[i][0], positions[i][1], positions[j][0], positions[j][1], fill="black", width=2)
        # draw vertices and numbers
        for i in range(n):
            if (i + 1) in self.longest_comp:
                canvas.create_oval(positions[i][0] - r, positions[i][1] - r,
                                   positions[i][0] + r, positions[i][1] + r,
                                   fill="red", outline="black", width=3)
            else:
                canvas.create_oval(positions[i][0] - r, positions[i][1] - r,
                                   positions[i][0] + r, positions[i][1] + r,
                                   fill="lime", outline="black", width=3)
            canvas.create_text(positions[i][0],
                               positions[i][1],
                               text=i + 1, font=("Comic Sans", int(3 * r / 4), "bold"), anchor=tk.CENTER)

        canvas.pack()
        window.mainloop()

    def draw_with_weights(self):
        if self.adjacencyMatrix is None:
            print("Empty graph - cannot draw the graph.")
            return
        width = height = 800
        n = len(self.adjacencyMatrix)
        alfa = 2 * math.pi / n

        center_x = width / 2
        center_y = height / 2
        R = center_x * 3 / 4
        if n > 3:
            r = R / n
        else:
            r = R / n * 0.5

        window = tk.Tk()
        window.geometry("800x800")
        canvas = tk.Canvas(window, height=height, width=width, bg="white")

        positions = []
        # set positions of vertices
        for i in range(n):
            positions.append([0.0, 0.0])
            if n > 1:
                positions[i][0] = center_y + R * math.sin(i * alfa)
                positions[i][1] = center_x - R * math.cos(i * alfa)
            else:
                positions[i][0] = center_x
                positions[i][1] = center_y
        canvas.create_oval(center_x - R, center_y - R, center_x + R,
                           center_y + R, outline="blue", width=3, dash=(5, 1))
        # draw edges
        for i in range(1, n):
            for j in range(0, i):
                if self.adjacencyMatrix[i][j] == 1:
                    canvas.create_line(positions[i][0], positions[i][1], positions[j][0], positions[j][1], fill="black",
                                       width=2)
        # draw weights
        for i in range(1, n):
            for j in range(0, i):
                if self.adjacencyMatrix[i][j] == 1:
                    txt = canvas.create_text((positions[i][0] + positions[j][0]) / 2,
                                             (positions[i][1] + positions[j][1]) / 2,
                                             text=self.weights[(i + 1, j + 1)],
                                             font=("Comic Sans", int(3 * r / 6), "bold"))
                    rect = canvas.create_rectangle(
                        canvas.bbox(txt), fill="white", outline="black")
                    canvas.tag_lower(rect, txt)
        # draw vertices and numbers
        for i in range(n):
            if (i + 1) in self.longest_comp:
                canvas.create_oval(positions[i][0] - r, positions[i][1] - r,
                                   positions[i][0] + r, positions[i][1] + r,
                                   fill="red", outline="black", width=3)
            else:
                canvas.create_oval(positions[i][0] - r, positions[i][1] - r,
                                   positions[i][0] + r, positions[i][1] + r,
                                   fill="lime", outline="black", width=3)
            canvas.create_text(positions[i][0],
                               positions[i][1],
                               text=i + 1, font=("Comic Sans", int(3 * r / 4), "bold"), anchor=tk.CENTER)

        canvas.pack()
        window.mainloop()

    def components(self):
        nr = 0
        temp_graph = self.adjacencyList.copy()
        comps = [-1] * max(temp_graph.keys())

        for temp in list(temp_graph):
            if comps[temp - 1] == -1:
                nr += 1
                comps[temp - 1] = nr
                self.components_recursive(nr, temp, temp_graph, comps)

        comps_representation = defaultdict(list)

        for i in range(len(comps)):
            comps_representation[comps[i]].append(i + 1)

        max_number = 0
        max_number_length = 0

        for i in range(0, max(comps_representation.keys())):
            temp = len(comps_representation.get(i + 1))
            if (temp > max_number_length):
                max_number_length = temp
                max_number = i + 1
        longest_vert = comps_representation.get(max_number)
        return longest_vert

    def components_recursive(self, nr, vertex, graph, comps):
        for temp in graph[vertex]:
            if comps[temp - 1] == -1:
                comps[temp - 1] = nr
                self.components_recursive(nr, temp, graph, comps)

    def check_hamilton(self):

        first_node = 1
        number_of_nodes = len(self.adjacencyList.keys())
        path = [first_node]
        visited_nodes = [-1] * number_of_nodes
        visited_nodes[first_node - 1] = 1

        self.hamilton_recursive(self.adjacencyList, number_of_nodes, first_node, visited_nodes, path)
        try:
            hamilton_path
        except NameError:
            print("Graph is not hamiltonian.")
        else:
            print("Graph is hamiltonian. Found path:")
            print(hamilton_path)

    def hamilton_recursive(self, list, number_of_nodes, first_node, visited_nodes, path):

        if len(path) == number_of_nodes and path[0] in list[path[number_of_nodes - 1]]:
            path.append(path[0])
            global hamilton_path
            hamilton_path = path.copy()
            path.pop()

        for node in list[first_node]:
            if visited_nodes[node - 1] == -1:
                visited_nodes[node - 1] = 1
                path.append(node)

                self.hamilton_recursive(list, number_of_nodes, node, visited_nodes, path)
                visited_nodes[node - 1] = -1
                path.pop()

    def weights_of_edges(self, weight_min=1, weight_max=10):
        pair_list = []
        weights = []
        for i in range(0, len(self.adjacencyMatrix)):
            for j in range(0, i):
                if (self.adjacencyMatrix[i][j] == 1):
                    pair_list.append((i + 1, j + 1))
                    weights.append(random.randint(weight_min, weight_max))
        self.weightsOfEdges = weights

        return defaultdict(list, dict(zip(pair_list, weights)))
    
    def weights_of_edges_digraph(self, weight_min=1, weight_max=10):
        pair_list = []
        weights = []
        for i in range(0, len(self.adjacencyMatrix)):
            for j in range(0, len(self.adjacencyMatrix)):
                if (self.adjacencyMatrix[i][j] == 1):
                    pair_list.append((i + 1, j + 1))
                    r=0
                    while(r==0):
                        r = random.randint(weight_min, weight_max)
                    weights.append(r)
        self.weightsOfEdges = weights

        return defaultdict(list, dict(zip(pair_list, weights)))

    def init_weigth_matrix(self):
        index = 0

        for i in range(0, len(self.adjacencyMatrixWeights)):
            for j in range(0, i):
                if (self.adjacencyMatrixWeights[i][j] == 1):
                    self.adjacencyMatrixWeights[i][j] = self.weightsOfEdges[index]
                    self.adjacencyMatrixWeights[j][i] = self.adjacencyMatrixWeights[i][j]
                    index += 1

    def init_weigth_matrix_digraph(self):
        index = 0

        for i in range(0, len(self.adjacencyMatrixWeights)):
            for j in range(0, len(self.adjacencyMatrix)):
                if (self.adjacencyMatrixWeights[i][j] == 1):
                    self.adjacencyMatrixWeights[i][j] = self.weightsOfEdges[index]
                    index += 1

    def generate_distance_matrix(self):
        """
        Generate matrix which contains distance between each pair of vertices in graph
        Function run Dijkstra algorithm for each vertex in graph
        Parameters

        """
        distance_matrix = np.zeros(shape=self.adjacencyMatrixWeights.shape)
        vertices_number, _ = self.adjacencyMatrixWeights.shape
        for vertex in range(vertices_number):
            d_s, _ = dijkstra_algorithm(self.adjacencyMatrixWeights, vertex + 1)
            distance_matrix[vertex, :] = d_s

        return distance_matrix




    def prim_mst(self):
        A = defaultdict(list)
        sets = defaultdict(list)
        # MAKE-SET
        for k, v in self.adjacencyList.items():
            sets[k] = k
        # posortuj krawedzie niemalejaco wzgledem wag
        weights = sorted(self.weights_of_edges().items(), key=lambda x: x[1])
        for k, v in weights:
            tmp = (sets[k[0]] != sets[k[1]])
            if (tmp):
                A[k[0]].append(k[1])
                A[k[1]].append(k[0])
                # UNION
                temp = sets[k[0]]
                for i in range(1, len(sets) + 1):
                    if sets[i] == temp:
                        sets[i] = sets[k[1]]
        self.minimumSpanningTree = adj_list_to_adj_matrix(A)
        self.print_with_mst()

    def print_with_mst(self):
        if self.minimumSpanningTree is not None:
            width = height = 800
            n = len(self.adjacencyMatrix)
            alfa = 2 * math.pi / n

            center_x = width / 2
            center_y = height / 2
            R = center_x * 3 / 4
            if n > 3:
                r = R / n
            else:
                r = R / n * 0.5

            window = tk.Tk()
            window.geometry("800x800")
            canvas = tk.Canvas(window, height=height, width=width, bg="white")

            positions = []
            # set positions of vertices
            for i in range(n):
                positions.append([0.0, 0.0])
                if n > 1:
                    positions[i][0] = center_y + R * math.sin(i * alfa)
                    positions[i][1] = center_x - R * math.cos(i * alfa)
                else:
                    positions[i][0] = center_x
                    positions[i][1] = center_y
            canvas.create_oval(center_x - R, center_y - R, center_x + R,
                               center_y + R, outline="blue", width=3, dash=(5, 1))
            # draw edges
            for i in range(1, n):
                for j in range(0, i):
                    if self.adjacencyMatrix[i][j] == 1:
                        if self.minimumSpanningTree[i][j] == 1:
                            canvas.create_line(positions[i][0], positions[i][1], positions[j][0], positions[j][1],
                                               fill="lime", width=2)
                        else:
                            canvas.create_line(positions[i][0], positions[i][1], positions[j][0], positions[j][1],
                                               fill="black", width=2)
            # draw weights
            for i in range(1, n):
                for j in range(0, i):
                    if self.adjacencyMatrix[i][j] == 1:
                        if self.minimumSpanningTree[i][j] == 1:
                            txt = canvas.create_text((positions[i][0] + positions[j][0]) / 2,
                                                     (positions[i][1] + positions[j][1]) / 2,
                                                     text=self.weights[(i + 1, j + 1)],
                                                     font=("Comic Sans", int(3 * r / 6), "bold"))
                            rect = canvas.create_rectangle(canvas.bbox(txt), fill="lime")
                            canvas.tag_lower(rect, txt)
                        else:
                            txt = canvas.create_text((positions[i][0] + positions[j][0]) / 2,
                                                     (positions[i][1] + positions[j][1]) / 2,
                                                     text=self.weights[(i + 1, j + 1)],
                                                     font=("Comic Sans", int(3 * r / 6), "bold"))
                            rect = canvas.create_rectangle(canvas.bbox(txt), fill="white", outline="black")
                            canvas.tag_lower(rect, txt)
            # draw vertices and numbers
            for i in range(n):
                if (i + 1) in self.longest_comp:
                    canvas.create_oval(positions[i][0] - r, positions[i][1] - r,
                                       positions[i][0] + r, positions[i][1] + r,
                                       fill="red", outline="black", width=3)
                else:
                    canvas.create_oval(positions[i][0] - r, positions[i][1] - r,
                                       positions[i][0] + r, positions[i][1] + r,
                                       fill="lime", outline="black", width=3)
                canvas.create_text(positions[i][0],
                                   positions[i][1],
                                   text=i + 1, font=("Comic Sans", int(3 * r / 4), "bold"), anchor=tk.CENTER)

            canvas.pack()
            window.mainloop()

    def digraph_from_a_m(self, a_m):
        self.adjacencyMatrix = a_m
        self.adjacencyMatrixWeights = a_m.copy()
        self.adjacencyList = adj_matrix_to_adj_list(a_m)
        self.incidenceMatrix = digraph_inc_m_from_adj_m(self.adjacencyMatrix)
        self.weights = self.weights_of_edges_digraph(-5, 10)
        self.init_weigth_matrix_digraph()

    def kosaraju(self):
        if (len(self.adjacencyList) != len(self.adjacencyMatrix)):
            return None
        d = {k: -1 for k, v in self.adjacencyList.items()}
        f = {k: -1 for k, v in self.adjacencyList.items()}
        t = 0
        for k, v in self.adjacencyList.items():
            if d[k] == -1:
                t = dfs_visit(k, self, d, f, t)
        adj_list_T = defaultdict(list)
        for k, v in self.adjacencyList.items():
            for e in v:
                adj_list_T[e].append(k)
        graph_T = Graph(adj_list_T, 'a_l')
        nr = 0
        comp = {k: -1 for k, v in graph_T.adjacencyList.items()}
        for k, v in sorted(graph_T.adjacencyList.items(), key=lambda x: x[1], reverse=True):
            if comp[k] == -1:
                nr += 1
                comp[k] = nr
                components_r(nr, k, graph_T, comp)
        return comp
      

    def distance_matrix(self):
        adj_m = self.adjacencyMatrixWeights.copy()
        n=len(adj_m)
        matrix = np.zeros((n, n))

        for s in range(n):
            row = bellman_ford(adj_m, s)
            if row is None:
                print("Cykl z ujemną sumą wag")
                return None
            matrix[s]=row
        
        print("Macierz odległości:")
        print(matrix)

def bellman_ford(adj_m, s=0):
    n = len(adj_m)
    row = np.full(n, np.inf)
    row[s] = 0

    for _ in range(n-1):
        for u in range(0, n):
            for v in range(0, n):
                w = adj_m[u][v]
                if (row[v] > (row[u] + w)) and w!=0:
                    row[v] = (row[u] + w)
    
    for u in range(0, n):
        for v in range(0, n):
            w = adj_m[u][v]
            if (row[v] > row[u] + w) and w != 0:
                return None
    return row

