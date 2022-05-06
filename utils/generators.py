from random import randrange
import numpy as np
from Graph import Graph
from degree_sequence import graphical_to_graph, is_graphical


def generate_n_l(vertices: int, edges: int, filename='') -> np.ndarray:
    """Graph adjacency matrix generation using number of vertices and number of edges.
    Function that generates graph's adjacency matrix based on input data. ValueError is raised when the input data
    is not valid. If file name is provided, function will save it's output into file.
    :param filename: (optional) Name of file to save adjacency matrix into.
    :param vertices: Number of vertices in graph. Must be higher than 0. It tells the size of output matrix.
    :param edges: Number of edges in graph. Must be in 0 to n(n-1)/2 range, where n is the number of vertices. It
        tells the number of 1's in triangular matrix created out of either upper or lower triangular matrix minus
        diagonal out of the output matrix.
    :return: Graph's adjacency matrix. It is a symmetrical 2D array of size (vertices x vertices), filled randomly
        with 0 or 1 based on entered number of edges. There are 0's on the diagonal.
    """

    msg = ''
    if vertices < 1:
        msg += 'Number of vertices must be higher than 0.\n'
    max_edges = vertices * (vertices - 1) // 2
    if 0 > edges or edges > max_edges:
        msg += f'Number of edges must be integer value in <0, {max_edges}> range.\n'
    if msg != '':
        raise ValueError(msg)
    else:
        indexes = np.zeros(max_edges)
        indexes[0:edges] = 1
        np.random.shuffle(indexes)
        a = np.zeros([vertices, vertices], dtype=int)
        a[np.triu_indices(vertices, 1)] = indexes
        a = a + a.T
        if filename != '':
            np.savetxt(filename, a, delimiter=' ', fmt='%d')
        return a


def generate_n_p(vertices: int, probability: float, filename='') -> np.ndarray:
    """Graph adjacency matrix generation using number of vertices and edge probability.
    Function that generates graph's adjacency matrix based on input data. ValueError is raised when the input data
    is not valid. If file name is provided, function will save it's output into file.
    :param filename: (optional) Name of file to save adjacency matrix into.
    :param vertices: Number of vertices in graph. Must be higher than 0. It tells the size of output matrix.
    :param probability: Probability of edge between two vertices. Must be in the 0 to 1 range. It is a probability
        of value 1 in the matrix.
    :return: Graph's adjacency matrix. It is a symmetrical 2D array of size (vertices x vertices), filled randomly
        with 0 or 1 based on entered probability value. There are 0's on the diagonal.
    """

    msg = ''
    if vertices < 1:
        msg += 'Number of vertices must be higher than 0.\n'
    if 0 > probability or probability > 1:
        msg += 'Probability must be in <0, 1> range.\n'
    if msg != '':
        raise ValueError(msg)
    else:
        a = np.triu(np.random.choice(2, size=[vertices, vertices], p=[1.0-probability, probability]))
        np.fill_diagonal(a, 0)
        a = a + a.T
        if filename != '':
            np.savetxt(filename, a, delimiter=' ', fmt='%d')
        return a


def generate_eulerian(vertices: int) -> Graph:
    msg = ''
    if vertices < 3:
        msg += 'Number of vertices must be higher than 2.\n'
    if msg != '':
        raise ValueError(msg)
    else:
        while True:
            degree_seq = [randrange(0, vertices, 2) for _ in range(vertices)]
            if is_graphical(degree_seq.copy()):
                break
        adj_list = graphical_to_graph(degree_seq)
        return Graph(adj_list, 'a_l')


if __name__ == '__main__':
    # print(generate_n_l(6, 1, 'test2.txt'))
    # print(generate_n_p(9, 0.5, 'test.txt'))
    generate_eulerian(8).draw()
