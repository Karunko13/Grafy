from conversions import *
from Graph import Graph
from degree_sequence import print_graphical

if __name__ == '__main__':
    g1 = Graph("z1_am.txt", "a_m")
    g1.print_all_representations()
    g1.draw()

    print_graphical([4,2,2,3,2,1,4,2,2,2,2])