import sys
from conversions import *
from Graph import Graph
from generators import *

if __name__ == '__main__':
    # g1 = Graph("z1_am.txt", "a_m", True)
    # g1.print_all_representations()
    # g1.draw()
    print(generate_n_l(12, 12, 'test2.txt'))
    #print(generate_n_p(9, 0.5, 'test.txt'))
    g1 = Graph("test2.txt", "a_m")
    g1.draw()

