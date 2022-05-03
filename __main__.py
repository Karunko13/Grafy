from utils.conversions import *
from utils.degree_sequence import *
from utils.generators import *
from Graph import Graph


if __name__ == '__main__':
    # g1 = Graph("txt_files/z1_am.txt", "a_m")
    # g1.print_all_representations()
    # g1.draw()
    # g1.components()
    #print_graphical([4,2,2,3,2,1,4,2,2,2,2])



    # g2 = graphical_to_graph([4,2,2,3,2,1,4,2,2,2,2])
    # g2.draw()
    # g2.check_hamilton()

    print(generate_n_l(12,5, 'txt_files/test.txt'))
    g3=Graph('txt_files/test.txt', "a_m")
    g3.draw()