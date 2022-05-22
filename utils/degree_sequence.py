from Graph import Graph
import numpy as np
from collections import OrderedDict, defaultdict

def is_graphical(A):
    n = sum(1 for x in A if x % 2 == 1)
    if n % 2 == 1:
        return False
    A.sort(reverse=True)
    while True:
        if all(x == 0 for x in A):
            return True
        if A[0] < 0 or A[0] >= len(A) or any(x < 0 for x in A):
            return False
        for i in range (1, A[0]+1):
            A[i] -= 1
        A[0] = 0
        A.sort(reverse=True)


# print (is_graphical([4,2,2,3,2,1,4,2,2,2,2]))
# print (is_graphical([4,4,3,1,2]))
# print (is_graphical([6,5,4,4,3,3,2]))
# print (is_graphical([3,3,2,2,2]))
# print (is_graphical([0]))

def graphical_to_graph(A):
    if is_graphical(A.copy()):
        A.sort(reverse=True)
        A_dict = OrderedDict( {i+1 : A[i] for i in range(0, len(A))} )
        adj_l = defaultdict(list)
        while True:
            item = A_dict.popitem(last=False)
            for index, element in enumerate(A_dict.items()):
                if index < item[1]:
                    A_dict[element[0]] -= 1
                    adj_l[element[0]].append(item[0])
                    adj_l[item[0]].append(element[0])
            A_dict = OrderedDict(sorted(A_dict.items(), key=lambda x: x[1], reverse=True))
            if all(x==0 for x in A_dict):
                break
        #return Graph(adj_l, 'a_l', False)
        return adj_l
    else:
        raise ValueError('not graphical')

def print_graphical(A):
    try:
        a = Graph(graphical_to_graph(A), 'a_l', False)
        a.draw()
    except ValueError as e:
        print(e.args)

# if __name__ == '__main__':
#     print_graphical([4,2,2,3,2,1,4,2,2,2,2])
#     print_graphical([4,4,3,1,2])