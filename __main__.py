from Graph import Graph
import os

from utils.generators import generate_eulerian
from utils.regular_graph_randomization import *
from utils.degree_sequence import *
from utils.euler import get_euler_cycle, pretty_cycle_print
from utils.generators import *


def zestaw1():
    #ZESTAW 1
    print("\nZESTAW 1\n")
    #zad1
    print("\nzad1\n")
    g1_am = Graph("txt_files/z1_am.txt", "a_m")
    g2_al = Graph("txt_files/z1_al.txt", "a_l")
    g3_im = Graph("txt_files/z1_im.txt", "i_m")
    g1_am.print_all_representations()
    
    #zad2
    print("\nzad2\n")
    g1_am.draw("zestaw1/zad2")
    
    #zad3
    print("\nzad3\n")
    generated_nl=Graph(generate_n_l(15,5), "a_m")
    generated_nl.draw("zestaw1/zad3 - n_l")
    
    generated_np=Graph(generate_n_p(8,0.3), "a_m")
    generated_np.draw("zestaw1/zad3 - n_p")

def zestaw2():
    #ZESTAW 2
    print("\nZESTAW 2\n")
    #zad1
    print("\nzad1\n")
    print_graphical([4,2,2,3,2,1,4,2,2,2,2], "zestaw2/zad1")

    #zad2
    print("\nzad2\n")
    random_graph = Graph(randomize_graph([4,2,2,3,2,1,4,2,2,2,2], 10), "a_l")
    random_graph.draw("zestaw2/zad2")
    
    #zad3
    print("\nzad3\n")
    generated=Graph(generate_n_l(15,5), "a_m")
    generated.draw("zestaw2/zad3")
    print(generated.longest_comp)
    
    #zad4
    # TO DO zmienic na metode graph
    print("\nzad4\n")
    generated_eul = Graph(generate_eulerian(7), 'a_l')
    res = get_euler_cycle(generated_eul.adjacencyList)  # Wyznaczanie cyklu Eulera
    pretty_cycle_print(res)  # Wypisywanie cyklu Eulera
    generated_eul.draw("zestaw2/zad4")
    
    #zad5
    print("\nzad5\n")
    k_regular_graph = generate_k_regular_graph(6, 3)
    k_regular_graph.draw("zestaw2/zad5")
    
    #zad6
    print("\nzad6\n")
    lewis_hamilton = Graph("txt_files/z2_ham.txt", "a_m")
    lewis_hamilton.check_hamilton()
    lewis_hamilton.draw("zestaw2/zad6")
    
    
if __name__ == '__main__':
    
    os.system('cls')
    zestaw1()
    zestaw2()
    