from utils.conversions import *
from utils.degree_sequence import *
from utils.generators import *
from Graph import Graph


if __name__ == '__main__':
    g1 = Graph("txt_files/z1_am.txt", "a_m", True)
   # g1.print_all_representations()
    g1.draw()
    #g1.components()
    #print_graphical([4,2,2,3,2,1,4,2,2,2,2])

    g2 = graphical_to_graph([4,2,2,3,2,1,4,2,2,2,2])
    g2.draw()