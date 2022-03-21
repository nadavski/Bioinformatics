def InOutDegree(graph):
    deg_in = {node: 0 for node in set(list(graph.keys()) +
                                      [value for values in graph.values() for value in values])}
    deg_out = {node: 0 for node in set(list(graph.keys()) +
                                       [value for values in graph.values() for value in values])}
    for node in graph:
        deg_out[node] += len(graph[node])
        for vertex in graph[node]:
            deg_in[vertex] += 1
    return deg_in, deg_out

def IsolatedCycles(graph):
    cycles = []
    for node in graph:
        deg_in, deg_out = InOutDegree(graph)
        if deg_in[node] == 1 and deg_out[node] == 1:
            for vertex in graph[node]:
                if deg_in[vertex] == 1 and deg_out[vertex] == 1:
                    cur_cycle = [node, vertex]
                    cur_v = vertex
                    while (deg_in[cur_v] == 1 and deg_out[cur_v] == 1) and cur_v != node:
                        cur_v = graph[cur_v][0]
                        cur_cycle.append(cur_v)
                    if (set(cur_cycle) not in [set(cycle) for cycle in cycles]
                            and cur_cycle[0] == cur_cycle[-1]):
                        cycles.append(cur_cycle)
    return cycles

def MaximalNonBranchingPaths(graph: dict):
    deg_in, deg_out = InOutDegree(graph)
    paths = []
    used = []
    for node in graph:
        if not (deg_in[node] == 1 and deg_out[node] == 1) and deg_out[node] > 0:
            for vertex in graph[node]:
                cur_path = [node, vertex]
                cur_v = vertex
                while deg_in[cur_v] == 1 and deg_out[cur_v] == 1:
                    cur_v = graph[cur_v][0]
                    cur_path.append(cur_v)
                paths.append(cur_path)
            used.append(node)
    for node in used:
        del graph[node]
    paths.extend(IsolatedCycles(graph))
    return paths


with open('dataset.txt') as data:
    lines = data.readlines()
    graph = {}
    for line in lines:
        node, vertices = line.strip().split(' -> ')
        graph[int(node)] = list(map(int, vertices.split(',')))
    print('MaximalNonBranchingPaths Implementation - In file "max_nonbranching_paths.txt"')
with open('max_nonbranching_paths.txt', 'w') as data:
    for path in MaximalNonBranchingPaths(graph):
        data.writelines(['->'.join(map(str, path)) + '\n'])
