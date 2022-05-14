# from utils.conversions import *
# from utils.degree_sequence import *
from utils.generators import generate_eulerian
from utils.regular_graph_randomization import *
from utils.euler import get_euler_cycle, pretty_cycle_print
from Graph import Graph
from utils.dijkstra import *
from utils.generators import *

def print_array(arr):
    """
    prints a 2-D numpy array in a nicer format
    """
    for a in arr:
        for elem in a:
            print(f"{elem:<2.0f}".rjust(3), end="")
        print(end="\n")



if __name__ == '__main__':
    g1 = Graph("z1_am.txt", "a_m")
    # g1.print_all_representations()
    print(g1.weights)
    print(g1.weightsOfEdges)
    distance_matrix, previous_matrix = dijkstra_algorithm(g1.adjacencyMatrixWeights)
    print_array(g1.adjacencyMatrixWeights)
    print_dijkstra_algorithm_result(distance_matrix, previous_matrix)

    print_array(g1.distanceMatrix)

    g1.draw_with_weights()
    # g1.prim_mst()
    # g1.components()
    #print_graphical([4,2,2,3,2,1,4,2,2,2,2])

    # g2 = graphical_to_graph([4,2,2,3,2,1,4,2,2,2,2])
    # g2.draw()
    # g2.check_hamilton()

    # print(generate_n_l(12,5, 'txt_files/test.txt'))
    # g3=Graph('txt_files/test.txt', "a_m")
    # g3.draw()

    # g2 = Graph(randomize_graph([4,2,2,3,2,1,4,2,2,2,2], 10), "a_l")
    # g2.draw()

    # Zestaw 2. Zadanie 4:
    # test = generate_eulerian(8)  # Generacja grafu eulerowskiego
    # G = Graph(test, 'a_l')
    # res = get_euler_cycle(test)  # Wyznaczanie cyklu Eulera
    # pretty_cycle_print(res)  # Wypisywanie cyklu Eulera
    # G.draw()

    # #zad 5 k_regular graph
    # g3 = generate_k_regular_graph(6, 3)
    # g3.draw()
