from turtle import width
import numpy as np
import tkinter as tk
import math
import random
import copy


class FlowNetwork:
    adjacencyMatrix_MaxFlow = None  # macierz sasiedztwa z maksymalnym przepływem
    adjacencyMatrix_CurrFlow = None  # macierz sasiedztwa z aktualnym przepływem
    layers_with_vertices = None  # warstwy z wierzchołkami
    vertices_in_layers = None

    def __init__(self, adj_matrix=None, layers_with_vertices=None, vertices_in_layers=None):

        self.adjacencyMatrix_MaxFlow = adj_matrix
        self.adjacencyMatrix_CurrFlow = np.zeros(
            (len(adj_matrix), len(adj_matrix)), int)
        self.layers_with_vertices = layers_with_vertices
        self.vertices_in_layers = vertices_in_layers

    def ford_fulkerson(self):
        path = []
        while self.bfs(path):
            cfp = path[0][2]
            for i in range(1, len(path)):
                if cfp > path[i][2]:
                    cfp = path[i][2]

            for egde in path:
                if self.adjacencyMatrix_MaxFlow[egde[0]][egde[1]]:
                    if self.adjacencyMatrix_MaxFlow[egde[0]][egde[1]] - self.adjacencyMatrix_CurrFlow[egde[0]][egde[1]] >= cfp:
                        self.adjacencyMatrix_CurrFlow[egde[0]][egde[1]] += cfp
                    else:
                        self.adjacencyMatrix_CurrFlow[egde[0]][egde[1]] -= cfp

            path = []

        s_out = self.adjacencyMatrix_CurrFlow[0].sum()  # fn.data[0][i][0]
        t_in = self.adjacencyMatrix_CurrFlow[:, -1].sum()

        print("Przepływ wypływający z początku: "+str(s_out)+"\nPrzepływ wpływający do końca: "+str(t_in))

    def bfs(self, path):
        d_s = [np.inf for _ in range(len(self.adjacencyMatrix_CurrFlow))]
        p_s = [-1 for _ in range(len(self.adjacencyMatrix_CurrFlow))]
        d_s[0] = 0

        queue = [0]
        while len(queue):
            v = queue.pop(0)
            for u in range(len(self.adjacencyMatrix_CurrFlow)):
                if self.adjacencyMatrix_MaxFlow[v][u] - self.adjacencyMatrix_CurrFlow[v][u]:
                    if d_s[u] == np.inf:
                        d_s[u] = d_s[v]+1
                        p_s[u] = v
                        queue.append(u)
            if p_s[len(self.adjacencyMatrix_CurrFlow)-1] != -1:
                break

        if p_s[len(self.adjacencyMatrix_CurrFlow)-1] != -1:
            v = len(self.adjacencyMatrix_CurrFlow)-1
            while v != 0:
                u = p_s[v]
                # print(u, v, self.adjacencyMatrix_MaxFlow[u][v])
                path.append([u, v, self.adjacencyMatrix_MaxFlow[u]
                            [v] - self.adjacencyMatrix_CurrFlow[u][v]])
                v = p_s[v]

            path.reverse()
        return(len(path))

    def draw(self, title="okno"):

        matrix_maxFlow = self.adjacencyMatrix_MaxFlow
        matrix_currFlow = self.adjacencyMatrix_CurrFlow
        origin_layers = self.vertices_in_layers
        curr_layers = origin_layers[1:len(origin_layers)-1]

        num_of_vertices = len(matrix_maxFlow)
        img_width = img_height = 800
        center_x = img_width / 2
        center_y = img_height / 2
        R = center_x * 3 / 5
        if num_of_vertices > 3:
            r = R / num_of_vertices
        else:
            r = R / num_of_vertices * 0.5

        window = tk.Tk()
        window.winfo_toplevel().title(title)
        window.geometry("800x800")
        canvas = tk.Canvas(window, height=img_height,
                           width=img_width, bg="white")

        vert_xy = []
        for i in range(num_of_vertices):
            vert_xy.append([0.0, 0.0])

        draw_layers = [[0]]

        # stworzenie "tablicy warstaw"
        temp = 1
        for layer in curr_layers:
            next_layer = []
            for i in range(layer):
                next_layer.append(temp)
                temp += 1
            draw_layers.append(next_layer)
        draw_layers.append([num_of_vertices-1])
        # draw layers reprezentuje warstwy rysowane w jednej płaszczyźnie
        num_layers = len(draw_layers)

        # podzielenie obszaru rysowania na rowne czesci
        layers_length = img_width / num_layers

        for i in range(len(draw_layers)):
            for j in range(len(draw_layers[i])):
                vert_xy[draw_layers[i][j]][0], vert_xy[draw_layers[i][j]][1] = layers_length/2 + layers_length * \
                    i, (img_height / (len(draw_layers[i])+1) +
                        j * img_height / (len(draw_layers[i])+1))

        # podpisanie pierwszego i ostatniego wierzchołka
        texts = [str(i) for i in range(num_of_vertices)]
        texts[0], texts[num_of_vertices-1] = 'P', 'K'

        # rysowanie wierzchołków
        for i in range(num_of_vertices):
            canvas.create_oval(vert_xy[i][0] - r, vert_xy[i][1] - r,
                               vert_xy[i][0] + r, vert_xy[i][1] + r,
                               fill="lime", outline="black")
            canvas.create_text(vert_xy[i][0], vert_xy[i][1],
                               fill="black", text=texts[i], font=("Comic Sans", int(3 * r / 4), "bold"))

        # rysowanie połączeń(krawędzi ze strzałkami)
        for i in range(num_of_vertices):
            for j in range(num_of_vertices):
                if matrix_maxFlow[i][j] > 0:
                    sign_of_vector = None
                    ver1_x = vert_xy[i][0]
                    ver1_y = vert_xy[i][1]

                    ver2_x = vert_xy[j][0]
                    ver2_y = vert_xy[j][1]

                    if not math.fabs(ver2_x - ver1_x) <= 10 ** -3:
                        sign_of_vector = -(ver2_y - ver1_y) / (ver2_x - ver1_x)

                    if ver1_x < ver2_x:
                        x_orientation = 1
                    else:
                        x_orientation = -1

                    if ver1_y < ver2_y:
                        y_orientation = 1
                    else:
                        y_orientation = -1

                    if math.fabs(ver2_x - ver1_x) <= 10 ** -3:
                        x = 0
                        y = r
                    elif math.fabs(ver2_y - ver1_y) <= 10 ** -3:
                        x = r
                        y = 0
                    else:
                        x = math.sqrt(
                            r ** 2 / (sign_of_vector ** 2 + 1))
                        y = math.fabs(sign_of_vector * x)

                    canvas.create_line(ver1_x + x_orientation * x, ver1_y + y_orientation * y,
                                       ver2_x - x_orientation * x, ver2_y - y_orientation * y, fill="black", arrow=tk.LAST, width=1)
        # rysowanie wag
        for i in range(num_of_vertices):
            for j in range(num_of_vertices):
                if matrix_maxFlow[i][j] > 0:
                    txt = canvas.create_text((vert_xy[i][0] + vert_xy[j][0]) / 2,
                                             (vert_xy[i][1] +
                                              vert_xy[j][1]) / 2,
                                             text=f'{matrix_currFlow[i][j]}/{matrix_maxFlow[i][j]}',
                                             font=("Comic Sans", 12, "bold"))

                    rect = canvas.create_rectangle(
                        canvas.bbox(txt), fill="white", outline="black")
                    canvas.tag_lower(rect, txt)

        canvas.pack()
        window.mainloop()


    def print_flow(self):
        for i in range(0, len(self.adjacencyMatrix_MaxFlow)):
            for j in range(0, len(self.adjacencyMatrix_MaxFlow)):
                if self.adjacencyMatrix_MaxFlow[i][j]>0:
                    print("Krawędź: "+str(i)+"->"+str(j)+", przepływ: "+str(self.adjacencyMatrix_CurrFlow[i][j])+"/"+str(self.adjacencyMatrix_MaxFlow[i][j]))


def generate_am_for_flow_network(n_of_layers=2, weight_min=1, weight_max=10):
    vertices_in_layers = np.random.randint(2, n_of_layers+1, (n_of_layers+2))
    vertices_in_layers[0] = vertices_in_layers[n_of_layers+1] = 1

    adj_matrix = np.zeros(
        (sum(vertices_in_layers), sum(vertices_in_layers)), dtype=int)

    layers_with_vertices = []
    v = 0
    for layer in vertices_in_layers:
        layer_to_add = []
        for i in range(layer):
            layer_to_add.append(v)
            v += 1
        layers_with_vertices.append(layer_to_add)

    for i in range(len(layers_with_vertices)-1):
        layer1 = layers_with_vertices[i]
        layer2 = layers_with_vertices[i+1]
        layer1_cp = layer1[:]
        layer2_cp = layer2[:]
        while len(layer1_cp) > 0 or len(layer2_cp) > 0:
            len1 = len(layer1_cp)
            len2 = len(layer2_cp)
            v1 = layer1_cp[random.randint(0, len1-1)]
            v2 = layer2_cp[random.randint(0, len2-1)]
            adj_matrix[v1][v2] = random.randint(weight_min, weight_max)
            layer1_cp.remove(v1)
            layer2_cp.remove(v2)
            len1 -= 1
            len2 -= 1
            if len1 == 0 and len2 > 0:
                layer1_cp = layer1[:]
            elif len1 > 0 and len2 == 0:
                layer2_cp = layer2[:]
    k = 0
    while k < (2*n_of_layers):
        i = random.randint(0, len(adj_matrix)-2)
        j = random.randint(1, len(adj_matrix)-1)
        if(adj_matrix[i][j] == 0 and i != j and adj_matrix[j][i] == 0):
            adj_matrix[i][j] = random.randint(weight_min, weight_max)
        else:
            k -= 1
        k += 1

    return adj_matrix, layers_with_vertices, vertices_in_layers
