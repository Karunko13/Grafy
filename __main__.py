from utils.regular_graph_randomization import *
from Graph import Graph

if __name__ == '__main__':
    # g1 = Graph("z1_am.txt", "a_m")
    # g1.print_all_representations()
    # g1.draw()

    # print_graphical([4,2,2,3,2,1,4,2,2,2,2])
    #zad2
    #g2 = Graph(randomize_graph([4, 4, 3, 1, 2], 10), "a_l", False) #not graphical sequence
    g2 = Graph(randomize_graph([4, 2, 2, 3, 2, 1, 4, 2, 2, 2, 2], 10), "a_l", False)
    g2.draw()





    # #zad 5 k_regular graph
    # g3 = generate_k_regular_graph(6, 3)
    # g3.draw()
