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

    def draw(self, img_width=1200, img_height=1200):
        """ Draws the flow network in new window which pops up. The flow network should be represented by adjacency matrix.
            On each arc there is placed it's current flow F and maximum capacity C in the "F/C" format.
            Drawing a flow network is not always ideal because it draws arcs as straight-line arrows.
                Therefore, sometimes arcs overlap each other and it's difficult to match arc and it's flow.
                img_width - width of the popped window (in pixels)
                img_height - height of the popped window (in pixels)"""

        data = self.adjacencyMatrix_MaxFlow
        lays = self.vertices_in_layers
        data2 = self.adjacencyMatrix_CurrFlow
        layers = lays[1:len(lays)-1]
        # pod 0 obecny, pod 1 max
        n = len(data)
        print(data)
        v_r = img_width / (3 * n) * (1 if n > 2 else 0.5)

        root = tk.Tk()
        root.geometry(str(img_height) + "x" + str(img_width))
        canvas = tk.Canvas(root, height=img_height,
                           width=img_width, bg="white")

        positions = [[0.0] * 2 for _ in range(n)]

        draw_layers = [[0]]
        if layers is not None:
            v = 1
            for layer in layers:
                layer_to_add = []
                for i in range(layer):
                    layer_to_add.append(v)
                    v += 1
                draw_layers.append(layer_to_add)
        else:
            num_inner_vertices = n - 2
            num_inner_layers = math.ceil(math.sqrt(num_inner_vertices))
            vertices_to_add = [i for i in range(1, n - 1)]
            for i in range(num_inner_layers, 0, -1):
                layer_to_add = []
                num_of_vertices_to_add = math.ceil(
                    len(vertices_to_add) / float(i))
                for j in range(num_of_vertices_to_add):
                    layer_to_add.append(vertices_to_add[0])
                    vertices_to_add.remove(vertices_to_add[0])
                draw_layers.append(layer_to_add)
        draw_layers.append([n-1])
        num_layers = len(draw_layers)

        h_break = img_width / num_layers

        for i in range(len(draw_layers)):
            x_pos = h_break/2 + h_break * i
            v_break = img_height / (len(draw_layers[i])+1)

            for j in range(len(draw_layers[i])):
                positions[draw_layers[i][j]][0], positions[draw_layers[i]
                                                           [j]][1] = x_pos, (v_break + j * v_break)

        texts = [str(i) for i in range(n)]
        texts[0], texts[n-1] = 's', 't'
        for i in range(n):
            canvas.create_oval(positions[i][0] - v_r, positions[i][1] - v_r,
                               positions[i][0] + v_r, positions[i][1] + v_r,
                               fill="lime", outline="black")
            canvas.create_text(positions[i][0], positions[i][1],
                               fill="black", text=texts[i], font=("Verdana", 15))

        for i in range(n):
            for j in range(n):
                if data[i][j] > 0:
                    a = None
                    v1_x = positions[i][0]
                    v2_x = positions[j][0]

                    v1_y = positions[i][1]
                    v2_y = positions[j][1]

                    equal_x = math.fabs(v2_x - v1_x) <= 10 ** -3
                    equal_y = math.fabs(v2_y - v1_y) <= 10 ** -3
                    if not equal_x:
                        a = -(v2_y - v1_y) / (v2_x - v1_x)

                    x_sign = 1 if v1_x < v2_x else -1
                    y_sign = 1 if v1_y < v2_y else -1

                    x = 0 if equal_x else v_r if equal_y else math.sqrt(
                        v_r ** 2 / (a ** 2 + 1))
                    y = 0 if equal_y else v_r if equal_x else math.fabs(a * x)
                    canvas.create_line(v1_x + x_sign * x, v1_y + y_sign * y,
                                       v2_x - x_sign * x, v2_y - y_sign * y, fill="black", arrow=tk.LAST)

        for i in range(n):
            for j in range(n):
                if data[i][j] > 0:
                    txt = canvas.create_text((positions[i][0] + positions[j][0]) / 2,
                                             (positions[i][1] +
                                              positions[j][1]) / 2,
                                             text=f'{data2[i][j]}/{data[i][j]}',
                                             font=("Comic Sans", 12, "bold"))

                    rect = canvas.create_rectangle(
                        canvas.bbox(txt), fill="white", outline="black")
                    canvas.tag_lower(rect, txt)

        print("Flow network is being drawn.")
        canvas.pack()
        root.mainloop()


def generate_am_for_flow_network(n_of_layers=2, weight_min=1, weight_max=10):
    vertices_in_layers = np.random.randint(2, n_of_layers+1, (n_of_layers+2))
    vertices_in_layers[0] = vertices_in_layers[n_of_layers+1] = 1
    # print(vertices_in_layers)

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

    # print(layers_with_vertices)

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
