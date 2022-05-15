import random
from utils.degree_sequence import *
from Graph import Graph

def swap(x1, x2, y1, y2, adjacency_list):
    adjacency_list[x1].append(y1)
    adjacency_list[y1].append(x1)
    adjacency_list[x2].append(y2)
    adjacency_list[y2].append(x2)


def delete_edge(v1, v2, adjacency_list):
    adjacency_list[v1].remove(v2)
    adjacency_list[v2].remove(v1)


def randomize_graph(degree_sequence, number_of_swaps):
    """
    Randomize graph by swaping edges few times

    :param degree_sequence: sequence of natural numbers
    :param number_of_swaps: number of edge swaping
    :return: adjacency list of graph
    """

    adjacency_list = graphical_to_graph(degree_sequence)

    for _ in range(number_of_swaps):
        while True:
            x1, y1 = random.sample(list(adjacency_list.keys()), k=2)

            if y1 not in adjacency_list[x1] and len(adjacency_list[x1]) > 0 and len(adjacency_list[y1]) > 0:

                x2 = random.sample([vertex for vertex in adjacency_list[x1] if vertex != x1], k=1)[0]
                y2 = random.sample([vertex for vertex in adjacency_list[y1] if vertex != y1], k=1)[0]
                if x2 == y2 or y2 in adjacency_list[x2] and (x2 in adjacency_list[y1] or y2 in adjacency_list[x1]):
                    pass
                else:
                    delete_edge(x1, x2, adjacency_list)
                    delete_edge(y1, y2, adjacency_list)
                    if x2 not in adjacency_list[y2]:
                        swap(x1, x2, y1, y2, adjacency_list)
                    else:
                        swap(x1, x2, y2, y1, adjacency_list)
                    break

    return adjacency_list


def generate_k_regular_graph(vertices_number, k):
    """
    Generating a k-regular graph based on number of vercites and degree(k)

    :param vertices_number: number of vertices in graph
    :param k: number of edges in every from every single vertex
    :return: Regular Graph
    """


    if (vertices_number >= k + 1 and vertices_number * k % 2 == 0):
        degree_sequence = [k] * vertices_number
        adj_list = randomize_graph(degree_sequence, 10)
        return Graph(adj_list, 'a_l')
