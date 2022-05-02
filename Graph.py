from turtle import position
from utils.conversions import *
import tkinter as tk
import math

class Graph:
    adjacencyMatrix = None  # macierz sasiedztwa
    adjacencyList = None  # lista sasiedztwa
    incidenceMatrix = None  # macierz incydencji
    longest_comp = None # najdłuższa spójna składowa
    
    def __init__(self, file_path=None, graph_representation="a_m"):
        if type(file_path) is str:
            if file_path is None:
                data = [[None]]
            else:
                with open(file_path, 'r') as f:
                    data = [[int(val) for val in line.split(' ')] if line != '\n' else [] for line in f]

            print("Graph represented by " + ("adjacency matrix." if graph_representation == "a_m"
                                            else ("incidence matrix." if graph_representation == "i_m" else "adjacency list.")))
        else:
            data = file_path

        if graph_representation == "a_m":
            self.adjacencyMatrix = np.copy(data)
            self.adjacencyList = adj_matrix_to_adj_list(self.adjacencyMatrix)
            self.incidenceMatrix = adj_matrix_to_inc_matrix(self.adjacencyMatrix)
        elif graph_representation == "i_m":
            self.incidenceMatrix = np.copy(data)
            self.adjacencyMatrix = inc_matrix_to_adj_matrix(self.incidenceMatrix)
            self.adjacencyList = inc_matrix_to_adj_list(self.incidenceMatrix)
        else:
            if type(file_path) is str:
                key_values = list(range(1,len(data)+1))
                list_of_dict = defaultdict(list, dict(zip(key_values, data)))

                self.adjacencyList = list_of_dict
                self.adjacencyMatrix = adj_list_to_adj_matrix(self.adjacencyList)
                self.incidenceMatrix = adj_list_to_inc_matrix(self.adjacencyList)

            else:
                self.adjacencyList = data
                self.adjacencyMatrix = adj_list_to_adj_matrix(self.adjacencyList)
                self.incidenceMatrix = adj_list_to_inc_matrix(self.adjacencyList)

        self.longest_comp = self.components()
            
    def __str__(self):
        return str(self.print_all_representations())

    def print_all_representations(self):
        print(self.adjacencyList)
        print(self.adjacencyMatrix)
        print(self.incidenceMatrix)

    def draw(self):
        if self.adjacencyMatrix is None:
            print("Empty graph - cannot draw the graph.")
            return
        width = height = 800
        n = len(self.adjacencyMatrix)
        alfa = 2 * math.pi / n

        center_x = width / 2
        center_y = height / 2
        R = center_x * 3/4
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
        #draw edges
        for i in range(1, n):
            for j in range(0, i):
                if self.adjacencyMatrix[i][j] == 1:
                    canvas.create_line(
                        positions[i][0], positions[i][1], positions[j][0], positions[j][1], fill="black", width=2)
        #draw vertices and numbers
        for i in range(n):
            if (i+1) in self.longest_comp:
                canvas.create_oval(positions[i][0]-r, positions[i][1]-r,
                                positions[i][0]+r, positions[i][1]+r,
                                fill="red", outline="black", width=3)
            else:
                canvas.create_oval(positions[i][0]-r, positions[i][1]-r,
                                   positions[i][0]+r, positions[i][1]+r,
                                   fill="lime", outline="black", width=3)
            canvas.create_text(positions[i][0],
                               positions[i][1],
                               text=i+1, font=("Comic Sans", int(3*r/4), "bold"), anchor=tk.CENTER)

        canvas.pack()
        window.mainloop()
    
    def components(self):
        nr = 0
        temp_graph = self.adjacencyList.copy()
        #print(temp_graph)
        comps = [-1]*len(temp_graph.keys())

        for temp in list(temp_graph):
            if comps[temp-1] == -1:
                nr += 1
                comps[temp-1] = nr
                self.components_recursive(nr, temp, temp_graph, comps)
        
        comps_representation = defaultdict(list)

        for i in range(len(comps)):
            comps_representation[comps[i]].append(i+1)

        max_number = 0
        max_number_length = 0

        for i in range(len(comps_representation.keys())):
            temp = len(comps_representation.get(i+1))
            if(temp > max_number_length):
                max_number_length = temp
                max_number = i+1
        longest_vert = comps_representation.get(max_number)
        return longest_vert

    def components_recursive(self, nr, vertex, graph, comps):
        for temp in graph[vertex]:
            if comps[temp-1] == -1:
                    comps[temp-1] = nr
                    self.components_recursive(nr, temp, graph, comps)

    
    # def check_hamilton(self):

    #     temp_list = self.adjacencyList
    #     first_node = 1
    #     number_of_nodes = len(temp_list.keys())
    #     path = [first_node]
    #     visited_nodes = [-1]*number_of_nodes
    #     visited_nodes[first_node-1] = 1
        
    #     print(number_of_nodes)
    #     print(path)
    #     print(visited_nodes)
    #     #self.hamilton_recursive(temp_list, number_of_nodes, first_node, visited_nodes, path)

    # def hamilton_recursive(self,temp_list, number_of_nodes, first_node, visited_nodes, path):
        
    #     if len(path) == number_of_nodes and path[0] in temp_list[path[number_of_nodes-1]]:
    #         print(path)
        
    #     for node in temp_list[first_node]:
    #         if not visited_nodes[node]:
    #             visited_nodes[node] = 1
    #             path.append(node)

    #             self.hamilton_recursive(temp_list, number_of_nodes, node, visited_nodes, path)
    #             visited_nodes[node] = -1
    #             path.pop()




