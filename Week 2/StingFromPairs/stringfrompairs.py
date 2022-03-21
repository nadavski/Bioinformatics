
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



def StringSpelledByGappedPatterns(patterns, k, d):
    first = ''
    second = ''
    for i in range(len(patterns) - 1):
        first += patterns[i][0][0]
        second += patterns[i][1][0]
    first += patterns[-1][0]
    second += patterns[-1][1]
    string_length = 2 * k + d + len(patterns) - 1
    nonoverlap_length = string_length - len(first)
    if first[nonoverlap_length:] == second[: -nonoverlap_length]:
        return first + second[-nonoverlap_length:]
    return
def DeBruijnFromPairedKmers(patterns):
    graph = {}
    for pattern in patterns:
        graph[pattern[0][:-1] + '|' + pattern[1][:-1]] = []
        graph[pattern[0][1:] + '|' + pattern[1][1:]] = []
    for pattern in patterns:
        graph[pattern[0][:-1] + '|' + pattern[1][:-1]].append(pattern[0][1:] + '|' + pattern[1][1:])
    return graph
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

def StringReconstructionFromReadPairs(patterns, k, d):
    graph = DeBruijnFromPairedKmers(patterns)
    eulerian_path = [pair.split('|') for pair in EulerianPath(graph)]
    string = StringSpelledByGappedPatterns(eulerian_path, k - 1, d + 1)
    return string


with open('dataset.txt') as data:
    lines = data.readlines()
    print(
        'String Reconstruction from Read-Pairs problem -',
        StringReconstructionFromReadPairs(
            [line.strip().split('|') for line in lines[1:]],
            *map(int.lines[0].strip().split())
        )
    )
