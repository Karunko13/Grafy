from turtle import position
from conversions import *
import tkinter as tk
import math

class Graph:
    adjacencyMatrix = None  # macierz sasiedztwa
    adjacencyList = None  # lista sasiedztwa
    incidenceMatrix = None  # macierz incydencji

    def __init__(self, file_path=None, graph_representation="a_m"):
        if file_path is None:
            data = [[None]]
        else:
            with open(file_path, 'r') as f:
                data = [[int(val) if '0' not in val else 0 for val in line.split(' ')] if line != '\n' else [] for
                        line in f]

        print("Graph represented by " + ("adjacency matrix." if graph_representation == "a_m"
                                         else ("incidence matrix." if graph_representation == "i_m" else "adjacency list.")))
        if graph_representation == "a_m":
            self.adjacencyMatrix = data
            self.adjacencyList = adj_matrix_to_adj_list(self.adjacencyMatrix)
            self.incidenceMatrix = adj_matrix_to_inc_matrix(
                self.adjacencyMatrix)
        elif graph_representation == "i_m":
            self.incidenceMatrix = data
            self.adjacencyMatrix = inc_matrix_to_adj_matrix(
                self.incidenceMatrix)
            self.adjacencyList = inc_matrix_to_adj_list(self.incidenceMatrix)
        else:
            self.adjacencyList = data
            self.adjacencyMatrix = adj_list_to_adj_matrix(self.adjacencyList)
            self.incidenceMatrix = adj_list_to_inc_matrix(self.adjacencyList)

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
        # set positions of verticles
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
        #draw verticles and numbers
        for i in range(n):
            canvas.create_oval(positions[i][0]-r, positions[i][1]-r,
                               positions[i][0]+r, positions[i][1]+r,
                               fill="lime", outline="black", width=3)
            canvas.create_text(positions[i][0],
                               positions[i][1],
                               text=i+1, font=("Comic Sans", int(3*r/4), "bold"), anchor=tk.CENTER)

        canvas.pack()
        window.mainloop()
