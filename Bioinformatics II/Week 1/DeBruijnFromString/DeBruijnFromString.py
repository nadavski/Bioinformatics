def DeBruijnFromString(text, k):
    graph = {text[i: i + k - 1]: list() for i in range(len(text) - k + 2)}
    for i in range(len(text) - k + 1):
        pattern = text[i: i + k]
        if pattern[:-1] in graph:
            graph[pattern[:-1]].append(pattern[1:])
    return graph


with open('sataset.txt') as data:
    lines = data.readlines()
    graph = DeBruijnFromString(lines[1].rstrip(), int(lines[0].rstrip()))

with open('de_bruijn_graph_from_string_answer.txt', 'w') as data:
    for node, patterns in graph.items():
        if patterns:
            data.writelines([node + '->' + ','.join(patterns) + '\n'])
    print('De Bruijn Graph from a String Problem -', 'In file "de_bruijn_graph_from_string_answer.txt"')

