import sys
from conversions import *
from Graph import Graph

if __name__ == '__main__':
    g1 = Graph("z1_am.txt", "a_m", True)
    #g1.print_all_representations()
    #print(g1.adjacencyList)
    g1.draw()

