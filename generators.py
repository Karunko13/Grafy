import numpy as np


def generate_n_p(vertices: int, probability: float) -> np.ndarray:
    """Graph adjacency matrix generation using number of vertices and edge probability.

    Function that generates graph's adjacency matrix based on input data. ValueError is raised when the input data
    is not valid.

    :param vertices: Number of vertices in graph. Must be higher than 0. It tells the size of output matrix.
    :param probability: Probability of edge between two vertices. Must be in the 0 to 1 range. It is a probability
        of value 1 in the matrix.
    :return: Graph's adjacency matrix. It is a symmetrical 2D array of size (vertices x vertices), filled randomly
        with 0 or 1, based on entered probability value. There are 0's on the diagonal.
    """

    msg = ''
    if vertices < 1:
        msg += 'Number of vertices must be higher than 0.\n'
    if probability < 0 or probability > 1:
        msg += 'Probability must be in <0, 1> range.\n'
    if msg != '':
        raise ValueError(msg)
    else:
        a = np.triu(np.random.choice(2, size=[vertices, vertices], p=[1.0-probability, probability]))
        np.fill_diagonal(a, 0)
        return a + a.T


if __name__ == '__main__':
    print(generate_n_p(9, 0.2))
