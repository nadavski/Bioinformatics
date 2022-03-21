import random


def EulerianCycle(graph: dict, start):
    if not graph:
        return
    cur_cycle = [start]
    euler_cycle = []
    while cur_cycle:
        cur_v = cur_cycle[-1]
        if graph[cur_v]:
            next_v = graph[cur_v].pop()
            cur_cycle.append(next_v)
        else:
            euler_cycle.append(cur_cycle.pop())
    return euler_cycle[::-1]


def EulerianPath(graph: dict):
    deg_in_minus_deg_out = {node: 0 for node in set(list(graph.keys()) +
                                                    [value for values in graph.values() for value in values])}
    for node in graph:
        deg_in_minus_deg_out[node] -= len(graph[node])
        for vertex in graph[node]:
            deg_in_minus_deg_out[vertex] += 1
    start = [node for node in deg_in_minus_deg_out if deg_in_minus_deg_out[node] == -1]
    end = [node for node in deg_in_minus_deg_out if deg_in_minus_deg_out[node] == 1]
    graph[end[0]] = [start[0]]
    eulerian_path = EulerianCycle(graph, start[0])
    eulerian_path.pop()
    return eulerian_path


with open('dataset.txt') as data:
    lines = data.readlines()
    graph = {}
    for line in lines:
        node, vertices = line.strip().split(' -> ')
        graph[int(node)] = list(map(int, vertices.split(',')))
    print(
        'Eulerian Path Problem -', '\n',
        '->'.join(map(str, EulerianPath(graph)))
    )
