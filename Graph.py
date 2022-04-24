from conversions import *
import tkinter as tk
import math
class Graph:
    adjacencyMatrix = None #macierz sasiedztwa
    adjacencyList = None #lista sasiedztwa
    incidenceMatrix = None #macierz incydencji
    temp = None
    
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

    def draw(self, img_width=600, img_height=600):
        
        print("here")
        print(self.adjacencyMatrix)
        self.temp = self.adjacencyMatrix

        if self.temp is None:
            print("Graph is empty (no temp) - cannot draw the graph.")
            return

        n = len(self.temp)
        angle = 2 * math.pi / n

        g_center_width = img_width / 2
        g_center_height = img_height / 2
        g_r = g_center_width * 2 / 3
        v_r = g_r / n * (1 if n > 2 else 0.5)

        root = tk.Tk()
        root.geometry(str(img_height)+"x"+str(img_width))
        canvas = tk.Canvas(root, height=img_height, width=img_width, bg="white")

        positions = [[0.0]*2 for _ in range(n)]

        for i in range(n):
            v_angle = i * angle
            positions[i][0] = g_center_height + (g_r * math.sin(v_angle) if n > 1 else 0)
            positions[i][1] = g_center_width - (g_r * math.cos(v_angle) if n > 1 else 0)

            fill_color = "black"

            canvas.create_oval(positions[i][0]-v_r, positions[i][1]-v_r,
                               positions[i][0]+v_r, positions[i][1]+v_r,
                               fill=fill_color)
            canvas.create_text(positions[i][0] + (1 + n/7) * v_r * math.sin(v_angle),
                               positions[i][1] - (1 + n/7) * v_r * math.cos(v_angle),
                               text=i+1, font=("Verdana", max(int(20 - 2*n/10), 10)))
        for i in range(1, n):
            for j in range(0, i):
                if self.temp[i][j] is 1:
                    canvas.create_line(positions[i][0], positions[i][1], positions[j][0], positions[j][1], fill="black")

        canvas.pack()
        root.mainloop()
