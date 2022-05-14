import numpy as np
from typing import List, Tuple

def init(vertices_number, start_vertex):
    """
    Set initial values of "distance" and "previous" array

    """

    d_s = np.full(vertices_number, np.Inf)
    p_s = np.full(vertices_number, np.nan)
    d_s[start_vertex] = 0
    return d_s, p_s


def relax(u, v, w, d_s, p_s):
    if d_s[v] > d_s[u] + w:
        d_s[v] = d_s[u] + w
        p_s[v] = u


def find_vertex_with_min_d_s(S, d_s):


    vertex_with_min_distance = 0
    min_weight = np.Inf
    for index, weight in enumerate(d_s):
        if index in S:
            continue
        if weight < min_weight:
            vertex_with_min_distance = index
            min_weight = weight
    return vertex_with_min_distance


def dijkstra_algorithm(start_matrix, start_vertex = 1):
    """
    Implementation of Dijkstra algorithm
    """

    if np.any(start_matrix < 0):
        raise ValueError("Dijkstra's algorithm does not support negative edge weights")

    vertices_number, _ = start_matrix.shape
    start_vertex -= 1
    if start_vertex >= vertices_number or start_vertex < 0:
        raise ValueError(f"Value of start vertex must be between 1 and {vertices_number}")

    d_s, p_s = init(vertices_number, start_vertex)
    S = np.empty(0, dtype=np.int64)
    while len(S) != vertices_number:
        u = find_vertex_with_min_d_s(S, d_s)
        S = np.sort(np.concatenate((S, np.array([u]))))
        for v, w in enumerate(start_matrix[:, u]):
            if v in S or w == 0:
                continue
            relax(u, v, w, d_s, p_s)
    return d_s, p_s


def generate_shortest_paths(p_s):
    """
    Function generates path based on previous vertices stored in p_s

    """
    paths = [[] for _ in p_s]
    finished_vertices = []

    while len(p_s) != len(finished_vertices):
        for vertex, previous_vertex in enumerate(p_s):
            if vertex in finished_vertices:
                continue
            elif np.isnan(previous_vertex):
                paths[vertex].append(vertex + 1)
                finished_vertices.append(vertex)
            elif len(paths[int(previous_vertex)]) != 0:
                paths[vertex].extend([*paths[int(previous_vertex)], vertex + 1])
                finished_vertices.append(vertex)
    return paths


def print_dijkstra_algorithm_result(d_s, p_s):
    """
    Function for nice results printing of Dijkstra algorithm

    """
    start_vertex = np.isnan(p_s).argmax()
    paths = generate_shortest_paths(p_s)
    print("Shortest paths from start vertex to others\n")
    print(f"Start vertex: {start_vertex + 1}\n")
    for vertex, (length, path) in enumerate(zip(d_s, paths)):
        print(f'vertex: {vertex + 1:2.0f}; path length: {length:2.0f}; path: {path}')