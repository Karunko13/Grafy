import numpy as np


def init(vert_amount, start_node):
    distance_matrix = np.full(vert_amount, np.Inf)
    predecessors_matrix = np.full(vert_amount, np.nan)
    distance_matrix[start_node] = 0
    return distance_matrix, predecessors_matrix


def find_vertex_with_min_d_s(S, distance_matrix):
    """
    Function returns number of node with shortest distance
    :param S:
    :param distance_matrix:
    """

    vertex_with_min_distance = 0
    min_weight = np.Inf
    for index, weight in enumerate(distance_matrix):
        if index in S:
            continue
        if weight < min_weight:
            vertex_with_min_distance = index
            min_weight = weight
    return vertex_with_min_distance


def dijkstra_algorithm(w, start_node=1):
    """

    :param w: adj_matrix with weights
    :param start_node: vertex for which we calculate paths
    :return: array of distances and array of previous vertex
    """


    if np.any(w < 0):
        raise ValueError("Error - negatywne wagi krawedzi")

    nodes, _ = w.shape
    start_node = start_node - 1

    if start_node >= nodes or start_node < 0:
        raise ValueError(f"Wierzcholek startowy powinien byc pomiedzy 1 - {nodes}")

    distance_array, predecessors_array = init(nodes, start_node)
    S = np.empty(0, dtype=np.int64)
    while len(S) != nodes:
        u = find_vertex_with_min_d_s(S, distance_array)
        S = np.sort(np.concatenate((S, np.array([u]))))
        for v, weight in enumerate(w[:, u]):
            if v in S or weight == 0:
                continue
            if distance_array[v] > distance_array[u] + weight:
                distance_array[v] = distance_array[u] + weight
                predecessors_array[v] = u

    return distance_array, predecessors_array


def generate_shortest_paths(predecessors_array):
    """

    :param predecessors_array: array of previous nodes
    :return:
    """
    paths = [[] for _ in predecessors_array]
    done_verts = []

    while len(predecessors_array) != len(done_verts):
        for vertex, previous_vertex in enumerate(predecessors_array):
            if vertex in done_verts:
                continue
            elif np.isnan(previous_vertex):
                paths[vertex].append(vertex + 1)
                done_verts.append(vertex)
            elif len(paths[int(previous_vertex)]) != 0:
                paths[vertex].extend([*paths[int(previous_vertex)], vertex + 1])
                done_verts.append(vertex)
    return paths


def print_dijkstra_algorithm_result(distance, previous_array):
    start_vertex = np.isnan(previous_array).argmax()
    paths = generate_shortest_paths(previous_array)

    print(f"Wierzcholek startowy: {start_vertex + 1}\n")
    for vertex, (length, path) in enumerate(zip(distance, paths)):
        print(f'd({vertex + 1:2.0f}) = {length:2.0f} ===> {path}')
