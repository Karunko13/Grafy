import numpy as np
from Graph import Graph
import generators


def get_graph_centre(distance_matrix: np.ndarray):
    if np.any(distance_matrix):
        row_sums = np.sum(distance_matrix, axis=0)
        min_sum = row_sums.min()
        return np.flatnonzero(row_sums == min_sum) + 1, min_sum
    else:
        return


def get_graph_minmax_centre(distance_matrix: np.ndarray):
    if np.any(distance_matrix):
        row_max = np.max(distance_matrix, axis=0)
        min_max = row_max.min()
        return np.flatnonzero(row_max == min_max) + 1, min_max
    else:
        return
