from Graph import Graph
from Flow_Network import *
import os

from utils.generators import generate_eulerian
from utils.regular_graph_randomization import *
from utils.degree_sequence import *
from utils.euler import get_euler_cycle, pretty_cycle_print
from utils.dijkstra import *
from utils.generators import *
from utils.centres import *


def zestaw1():
    # ZESTAW 1
    print("\nZESTAW 1\n")
    # zad1
    print("\nzad1\n")
    g1_am = Graph("txt_files/z1_am.txt", "a_m")
    g2_al = Graph("txt_files/z1_al.txt", "a_l")
    g3_im = Graph("txt_files/z1_im.txt", "i_m")
    g1_am.print_all_representations()

    # zad2
    print("\nzad2\n")
    g1_am.draw("zestaw1/zad2")

    # zad3
    print("\nzad3\n")
    generated_nl = Graph(generate_n_l(15, 5), "a_m")
    generated_nl.draw("zestaw1/zad3 - n_l")

    generated_np = Graph(generate_n_p(8, 0.3), "a_m")
    generated_np.draw("zestaw1/zad3 - n_p")


def zestaw2():
    # ZESTAW 2
    print("\nZESTAW 2\n")
    # zad1
    print("\nzad1\n")
    print_graphical([4, 2, 2, 3, 2, 1, 4, 2, 2, 2, 2], "zestaw2/zad1")

    # zad2
    print("\nzad2\n")
    random_graph = Graph(randomize_graph(
        [4, 2, 2, 3, 2, 1, 4, 2, 2, 2, 2], 10), "a_l")
    random_graph.draw("zestaw2/zad2")

    # zad3
    print("\nzad3\n")
    generated = Graph(generate_n_l(15, 5), "a_m")
    generated.draw("zestaw2/zad3")
    print(generated.longest_comp)

    # zad4
    # TO DO zmienic na metode graph
    print("\nzad4\n")
    generated_eul = Graph(generate_eulerian(7), 'a_l')
    # Wyznaczanie cyklu Eulera
    res = get_euler_cycle(generated_eul.adjacencyList)
    pretty_cycle_print(res)  # Wypisywanie cyklu Eulera
    generated_eul.draw("zestaw2/zad4")

    # zad5
    print("\nzad5\n")
    k_regular_graph = generate_k_regular_graph(6, 3)
    k_regular_graph.draw("zestaw2/zad5")

    # zad6
    print("\nzad6\n")
    lewis_hamilton = Graph("txt_files/z2_ham.txt", "a_m")
    lewis_hamilton.check_hamilton()
    lewis_hamilton.draw("zestaw2/zad6")


def zestaw3():
    # ZESTAW 3
    print("\nZESTAW 3\n")
    # zad1
    print("\nzad1\n")
    g1 = Graph(generate_n_l(7, 12), "a_m")
    g1.draw_with_weights()
    # zad2
    print("\nzad2\n")
    distance_matrix, previous_matrix = dijkstra_algorithm(
        g1.adjacencyMatrixWeights, 2)
    print_dijkstra_algorithm_result(distance_matrix, previous_matrix)

    # zad3
    print("\nzad3\n")
    print("\nMacierz odleglosci\n")
    print(g1.distanceMatrix)

    # #zad4
    print("\nzad4\n")
    print(get_graph_centre(g1.distanceMatrix))
    print(get_graph_minmax_centre(g1.distanceMatrix))

    # zad5
    print("\nzad5\n")
    g1.kruskal_mst()


def zestaw4():
    # ZESTAW 4
    print("\nZESTAW 4\n")

    # zad1
    print("\nzad1")
    g1 = generate_digraph(6, 0.3)
    g1.print_all_representations()

    # zad2
    print("\nzad2\n")
    # g2 = Graph()
    am = np.copy([
        [0, 1, 1, 0, 1, 0, 0],
        [1, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    # g2.digraph_from_a_m(am)
    # print(g2.kosaraju())

    b = False
    while not b:
        g2 = generate_digraph(6, 0.1)
        if(g2.kosaraju() is not None):
            b = len(list(set(list((g2.kosaraju()).values())))) == 1
    g2.digraph_from_a_m(am)
    print(g2.kosaraju())

    # zad3
    print("\nzad3\n")
    g2.print_all_representations()
    g2.distance_matrix()

    # zad 4


if __name__ == '__main__':

    os.system('cls')
    # zestaw1()
    # zestaw2()
    # zestaw3()
    # zestaw4()
    adj_matrix, layers_with_vertices, vertices_in_layers = generate_am_for_flow_network(
        3)
    f1 = FlowNetwork(adj_matrix, layers_with_vertices, vertices_in_layers)
    f1.draw()
    # print(f1.adjacencyMatrix_MaxFlow)
    # print("====================D")
    # print(f1.layers_with_vertices)
    f1.ford_fulkerson()
    print(f1.adjacencyMatrix_CurrFlow)
    f1.draw()
