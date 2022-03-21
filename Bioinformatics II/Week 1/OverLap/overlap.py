def Overlap(patterns):
    graph = {pattern: set() for pattern in patterns}
    for node in graph:
        for pattern in patterns:
            if pattern[:-1] == node[1:]:
                graph[node].add(pattern)
    return graph


with open('dataset.txt') as data:
    graph = Overlap(data.read().splitlines())

with open('overlap_graph_answer.txt', 'w') as data:
    for node, patterns in graph.items():
        if patterns:
            data.writelines([node + '->' + ','.join(patterns) + '\n'])
    print('Overlap Graph Problem -', 'In file "overlap_graph_answer.txt"')
