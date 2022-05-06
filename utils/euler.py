import copy
from utils.generators import generate_eulerian
from Graph import Graph


def get_euler_cycle(graph: dict) -> list:
    def is_bridge(a_l: dict) -> bool:
        start = list(a_l)[0]
        visited = {}
        for vert in a_l:
            visited[vert] = -1
        visited[start] = 0
        S = [start]
        while len(S):
            b = S.pop()
            for a in a_l[b]:
                if a in visited and visited[a] == -1:
                    visited[a] = 0
                    S.append(a)
                visited[b] = 1
        return list(visited.values()).count(1) != len(a_l)

    graph_copy = copy.deepcopy(graph)
    euler_cycle = []
    u = list(graph_copy.keys())[0]
    while len(graph_copy):
        current_vertex = u
        for u in list(graph_copy[current_vertex]):
            graph_copy[u].remove(current_vertex)
            graph_copy[current_vertex].remove(u)
            bridge = is_bridge(graph_copy)
            if bridge:
                graph_copy[u].append(current_vertex)
                graph_copy[current_vertex].append(u)
            else:
                break
        if bridge:
            if current_vertex in graph_copy[u]:
                graph_copy[u].remove(current_vertex)
            if u in graph_copy[current_vertex]:
                graph_copy[current_vertex].remove(u)
            graph_copy.pop(current_vertex)
        if current_vertex != u:
            euler_cycle.append((current_vertex, u))
    return euler_cycle


def pretty_cycle_print(cycle: list):
    print('\n\n\nEuler Cycle:\n[', ''.join('{} - '.format(val[0]) for val in cycle) + f'{cycle[0][0]}' + ' ]\n\n\n')


if __name__ == '__main__':
    test = generate_eulerian(7)
    G = Graph(test, 'a_l')
    res = get_euler_cycle(test)
    pretty_cycle_print(res)
    G.draw()

