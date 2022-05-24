import numpy as np
import tkinter as tk
import math
import random
import copy

class FlowNetwork:
    adjacencyMatrix_MaxFlow = None  # macierz sasiedztwa z maksymalnym przepływem
    adjacencyMatrix_CurrFlow = None  # macierz sasiedztwa z aktualnym przepływem

    def __init__(self, adj_matrix=None):
        
        self.adjacencyMatrix_MaxFlow=np.copy(adj_matrix)
        self.adjacencyMatrix_CurFlow = np.zeros((len(adj_matrix), len(adj_matrix)), int)


def generate_am_for_flow_network(n_of_layers=2, weight_min=1, weight_max=10):
    vertices_in_layers = np.random.randint(2, n_of_layers+1, (n_of_layers+2))
    vertices_in_layers[0]=vertices_in_layers[n_of_layers+1]=1
    print(vertices_in_layers)

    adj_matrix=np.zeros((sum(vertices_in_layers), sum(vertices_in_layers)), int)

    layers_with_vertices = []
    v = 0
    for layer in vertices_in_layers:
        layer_to_add = []
        for i in range(layer):
            layer_to_add.append(v)
            v += 1
        layers_with_vertices.append(layer_to_add)
    
    print(layers_with_vertices)
    
    for i in range (len(layers_with_vertices)-1):
        layer1=layers_with_vertices[i]
        layer2=layers_with_vertices[i+1]
        layer1_cp=layer1[:]
        layer2_cp = layer2[:]
        while len(layer1_cp) > 0 or len(layer2_cp)>0:
            len1 = len(layer1_cp)
            len2 = len(layer2_cp)
            v1 = layer1_cp[random.randint(0, len1-1)]
            v2 = layer2_cp[random.randint(0, len2-1)]
            adj_matrix[v1][v2] = random.randint(weight_min, weight_max)
            layer1_cp.remove(v1)
            layer2_cp.remove(v2)
            len1-=1
            len2-=1
            if len1==0 and len2>0:
                layer1_cp = layer1[:]
            elif len1 > 0 and len2 == 0:
                layer2_cp = layer2[:]
    k=0
    while k <(2*n_of_layers):
        i=random.randint(0,len(adj_matrix)-2)
        j=random.randint(1, len(adj_matrix)-1)
        if(adj_matrix[i][j]==0 and i!=j):
            adj_matrix[i][j] = random.randint(weight_min, weight_max)
        else:
            k-=1
        k+=1
    
    return adj_matrix







        

