import itertools
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

def DeBruijnFromKmers(patterns):
    graph = {}
    for pattern in patterns:
        graph[pattern[:-1]] = []
        graph[pattern[1:]] = []
    for pattern in patterns:
        graph[pattern[:-1]].append(pattern[1:])
    return graph

def BinaryStrings(k):
    return [''.join(string) for string in itertools.product('01', repeat=k)]

def PathToGenome(path):
    text = path[0]
    for i in range(1, len(path)):
        text += path[i][-1]
    return text

def kUniversalCircularString(k):
    graph = DeBruijnFromKmers(BinaryStrings(k))
    eulerian_cycle = EulerianCycle(graph, start=random.choice(list(graph.keys())))
    circular_string = PathToGenome(eulerian_cycle)
    return circular_string[:-(k - 1)]


with open('dataset.txt') as data:
    print(
        'k-Universal Circular String Problem -', '\n\n', 
        kUniversalCircularString(
            int(data.readline().strip())
        )
    )
