def DeBruijnFromKmers(patterns):
    graph = {}
    for pattern in patterns:
        graph[pattern[:-1]] = []
        graph[pattern[1:]] = []
    for pattern in patterns:
        graph[pattern[:-1]].append(pattern[1:])
    return graph


with open('dataset.txt') as data:
    graph = DeBruijnFromKmers(data.read().splitlines())

with open('de_bruijn_graph_from_kmers_answer.txt', 'w') as data:
    for node, patterns in graph.items():
        if patterns:
            data.writelines([node + '->' + ','.join(patterns) + '\n'])
    print('de Bruijn Graph from k-mers Problem -', 'In file "de_bruijn_graph_from_kmers_answer.txt"')
