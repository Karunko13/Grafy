import random
from utils.degree_sequence import *
from Graph import Graph


def swap(x1, x2, y1, y2, a_l):
    a_l[x1].append(y1)
    a_l[y1].append(x1)
    a_l[x2].append(y2)
    a_l[y2].append(x2)


def delete_edge(v1, v2, a_l):
    a_l[v1].remove(v2)
    a_l[v2].remove(v1)


def randomize_graph(degree_sequence, number_of_swaps):
    """
    Randomize graph by swaping edges few times

    :param degree_sequence: sequence of natural numbers
    :param number_of_swaps: number of edge swaping
    :return: adjacency list of graph
    """

    a_l = graphical_to_graph(degree_sequence)

    for _ in range(number_of_swaps):
        while True:
            x1, y1 = random.sample(list(a_l.keys()), k=2)

            if y1 not in a_l[x1] and len(a_l[x1]) > 0 and len(a_l[y1]) > 0:

                x2 = random.sample([vertex for vertex in a_l[x1] if vertex != x1], k=1)[0]
                y2 = random.sample([vertex for vertex in a_l[y1] if vertex != y1], k=1)[0]
                if x2 == y2 or y2 in a_l[x2] and (x2 in a_l[y1] or y2 in a_l[x1]):
                    pass
                else:
                    delete_edge(x1, x2, a_l)
                    delete_edge(y1, y2, a_l)
                    if x2 not in a_l[y2]:
                        swap(x1, x2, y1, y2, a_l)
                    else:
                        swap(x1, x2, y2, y1, a_l)
                    break

    return a_l


def generate_k_regular_graph(nodes, k):
    """
    Generating a k-regular graph based on number of vercites and degree(k)

    :param nodes: number of vertices in graph
    :param k: number of edges in every from every single vertex
    :return: Regular Graph
    """

    if (nodes >= k + 1 and nodes * k % 2 == 0):
        degree_sequence = [k] * nodes
        adj_list = randomize_graph(degree_sequence, 10)
        return Graph(adj_list, 'a_l')
