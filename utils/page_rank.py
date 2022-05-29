import random
import numpy as np
from Graph import Graph


def quater_sum_of_vector(v):
    result = 0
    for elem in v:
        result += float(elem ** 2)
    return result


def matrixVectorMultiple(m, v):
    result = []

    for i in range(len(v)):
        resultList = []
        resultList = [m[j][i] * v[j] for j in range(len(v))]
        result.append(sum(resultList))

    return result


def page_rank_1(graph, d):

    if d < 0 or d > 1:
        raise ValueError("Nieprawidłowa wartość dla prawdopodobieństwa")

    adj_l = graph.adjacencyList
    nodes, _ = graph.adjacencyMatrix.shape
    freqTab = [0 for i in range(nodes)]
    currNodeIDX = 1
    nodeslist = []

    for i in range(nodes):
        if len(adj_l[i+1]) == 0:
            raise ValueError("Graf z wierzchołkiem bez krawedzi wyjsciowych")

    for i in range(nodes):
        nodeslist.append(i + 1)

    N = 1000000
    i = 0

    while i < N:
        if random.random() > d and len(adj_l[currNodeIDX - 1]) != 0:
            currNodeIDX = random.choice(list(adj_l[currNodeIDX - 1]))
        else:
            currNodeIDX = (random.choice(list(nodeslist)))

        freqTab[currNodeIDX - 1] = freqTab[currNodeIDX - 1] + 1
        i += 1

    print("Algorytm PageRank 1")
    for i, pr in enumerate(freqTab):
        print(i + 1, "==> PageRank = ", pr / N)


def page_rank_2(graph, d):

    if d < 0 or d > 1:
        raise ValueError("Nieprawidłowa wartość dla prawdopodobieństwa")

    nodes, _ = graph.adjacencyMatrix.shape
    adj_l = graph.adjacencyList
    P = np.zeros((nodes, nodes))
    A = graph.adjacencyMatrix

    for i in range(nodes):
        if len(adj_l[i+1]) == 0:
            raise ValueError("Graf z wirzcholkiem bez krawedzi wyjsciowych")

    p_vec = np.full(nodes, 1 / nodes)
    pt = np.zeros(nodes)
    const = float(d / nodes)

    for i in range(nodes):
        neighbours = len(adj_l[i+1])
        # print(neighbours)
        for j in range(nodes):
            P[i][j] = (1.0 - d) * A[i][j] / neighbours + const

    iter = 0
    sumP = 10.0
    sumC = 0.0
    while np.abs(sumP - sumC) > 0.0000000001:
        sumP = quater_sum_of_vector(p_vec)
        p_vec = matrixVectorMultiple(P, p_vec)
        sumC = quater_sum_of_vector(p_vec)
        iter += 1

    print("\nAlgorytm PageRank 2")
    print(f"Zbieżność uzyskano po {iter} iteracjach.")
    for i in range(len(p_vec)):
        print(i + 1, "==> PageRank = ", round(p_vec[i], 6))
