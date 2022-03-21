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


with open('dataset.txt') as data:
    lines = data.readlines()
    graph = {}
    for line in lines:
        node, vertices = line.strip().split(' -> ')
        graph[int(node)] = list(map(int, vertices.split(',')))
    print(
        'Eulerian Cycle Problem -',
        '->'.join(map(str, EulerianCycle(graph, random.choice(list(graph.keys())))))
    )
