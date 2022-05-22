# from Graph import Graph
import numpy as np


def dfs_visit(v, G, d, f, t):
    t = t + 1
    d[v] = t
    for u in G.adjacencyList[v]:
        if d[u] == -1:
            t = dfs_visit(u, G, d, f, t)
    t += 1
    f[v] = t
    return t


def components_r(nr, v, G, comp):
    for u in G.adjacencyList[v]:
        if comp[u] == -1:
            comp[u] = nr
            components_r(nr, u, G, comp)