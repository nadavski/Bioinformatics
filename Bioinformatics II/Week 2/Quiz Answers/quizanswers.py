# CODING CHALLENGES
print('CODING CHALLENGES ANSWERS:')

# Code Challenge: Solve the Eulerian Cycle Problem.
#       Input: The adjacency list of an Eulerian directed graph.
#       Output: An Eulerian cycle in this graph.
import random
import string


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


# Code Challenge: Solve the Eulerian Path Problem.
#       Input: The adjacency list of a directed graph that has an Eulerian path.
#       Output: An Eulerian path in this graph.
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


# Code Challenge: Solve the String Reconstruction Problem.
#       Input: An integer k followed by a list of k-mers Patterns.
#       Output: A string Text with k-mer composition equal to Patterns.
#       (If multiple answers exist, you may return any one.)
def DeBruijnFromKmers(patterns):
    graph = {}
    for pattern in patterns:
        graph[pattern[:-1]] = []
        graph[pattern[1:]] = []
    for pattern in patterns:
        graph[pattern[:-1]].append(pattern[1:])
    return graph


def PathToGenome(path):
    text = path[0]
    for i in range(1, len(path)):
        text += path[i][-1]
    return text


def StringReconstruction(patterns):
    graph = DeBruijnFromKmers(patterns)
    eulerian_path = EulerianPath(graph)
    genome = PathToGenome(eulerian_path)
    return genome

# Code Challenge: Solve the k-Universal Circular String Problem.
#       Input: An integer k.
#       Output: A k-universal circular string.
import itertools


def BinaryStrings(k):
    return [''.join(string) for string in itertools.product('01', repeat=k)]


def kUniversalCircularString(k):
    graph = DeBruijnFromKmers(BinaryStrings(k))
    eulerian_cycle = EulerianCycle(graph, start=random.choice(list(graph.keys())))
    circular_string = PathToGenome(eulerian_cycle)
    return circular_string[:-(k - 1)]



# Code Challenge: Implement StringSpelledByGappedPatterns.
#       Input: Integers k and d followed by a sequence of (k, d)-mers (a_1|b_1), … , (a_n|b_n) such that
#       Suffix(a_i|b_i) = Prefix(a_(i+1)|b_(i+1)) for 1 ≤ i ≤ n-1.
#       Output: A string Text of length k + d + k + n - 1 such that the i-th (k, d)-mer in Text is equal to (a_i|b_i)
#       for 1 ≤ i ≤ n (if such a string exists).
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


# Code Challenge: Solve the String Reconstruction from Read-Pairs Problem.
#       Input: Integers k and d followed by a collection of paired k-mers PairedReads.
#       Output: A string Text with (k, d)-mer composition equal to PairedReads.
def DeBruijnFromPairedKmers(patterns):
    graph = {}
    for pattern in patterns:
        graph[pattern[0][:-1] + '|' + pattern[1][:-1]] = []
        graph[pattern[0][1:] + '|' + pattern[1][1:]] = []
    for pattern in patterns:
        graph[pattern[0][:-1] + '|' + pattern[1][:-1]].append(pattern[0][1:] + '|' + pattern[1][1:])
    return graph


def StringReconstructionFromReadPairs(patterns, k, d):
    graph = DeBruijnFromPairedKmers(patterns)
    eulerian_path = [pair.split('|') for pair in EulerianPath(graph)]
    string = StringSpelledByGappedPatterns(eulerian_path, k - 1, d + 1)
    return string



# Code Challenge: Implement MaximalNonBranchingPaths.
#       Input: The adjacency list of a graph whose nodes are integers.
#       Output: The collection of all maximal nonbranching paths in this graph.
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


# Code Challenge: Solve the Contig Generation Problem.
# Contig Generation Problem: Generate the contigs from a collection of reads (with imperfect coverage).
#       Input: A collection of k-mers Patterns.
#       Output: All contigs in DeBruijn(Patterns).
def ContigGeneration(patterns):
    graph = DeBruijnFromKmers(patterns)
    return [PathToGenome(path) for path in MaximalNonBranchingPaths(graph)]



# ---------------------------------------------------------------------------------------------------------------------
# QUIZ 2
# Question 1: Give a linear string having the following 4-mer composition.
# AAAT
# AATG
# ACCC
# ACGC
# ATAC
# ATCA
# ATGC
# CAAA
# CACC
# CATA
# CATC
# CCAG
# CCCA
# CGCT
# CTCA
# GCAT
# GCTC
# TACG
# TCAC
# TCAT
# TGCA
print(
    '-----------------------------\n'
    'QUIZ 2 ANSWERS:\nQ1 -',
    StringReconstruction(
        ['AAAT',
         'AATG',
         'ACCC',
         'ACGC',
         'ATAC',
         'ATCA',
         'ATGC',
         'CAAA',
         'CACC',
         'CATA',
         'CATC',
         'CCAG',
         'CCCA',
         'CGCT',
         'CTCA',
         'GCAT',
         'GCTC',
         'TACG',
         'TCAC',
         'TCAT',
         'TGCA']
    )
)

# Question 2: Below is the adjacency list of a graph. What is the minimum number of edges we must add to this graph
# in order to make each node balanced?
# (You may add duplicate edges connecting the same two nodes, but do not add new nodes.)
# 1 -> 2,3,5
# 2 -> 1,4
# 3 -> 2,5
# 4 -> 1,2,5
# 5 -> 3
print('Q2 -', 3)

# Queston 3: There is a single (linear) string with the following (3,1)-mer composition. Find it.
# (ACC|ATA)
# (ACT|ATT)
# (ATA|TGA)
# (ATT|TGA)
# (CAC|GAT)
# (CCG|TAC)
# (CGA|ACT)
# (CTG|AGC)
# (CTG|TTC)
# (GAA|CTT)
# (GAT|CTG)
# (GAT|CTG)
# (TAC|GAT)
# (TCT|AAG)
# (TGA|GCT)
# (TGA|TCT)
# (TTC|GAA)
print(
    'Q3 -',
    StringReconstructionFromReadPairs(
        [line.split('|') for line in [
            'ACC|ATA',
            'ACT|ATT',
            'ATA|TGA',
            'ATT|TGA',
            'CAC|GAT',
            'CCG|TAC',
            'CGA|ACT',
            'CTG|AGC',
            'CTG|TTC',
            'GAA|CTT',
            'GAT|CTG',
            'GAT|CTG',
            'TAC|GAT',
            'TCT|AAG',
            'TGA|GCT',
            'TGA|TCT',
            'TTC|GAA']
         ],
        k=3,
        d=1
    ),
    '???????????'
)


# Question 4: True or False: every Eulerian path in the de Bruijn graph constructed from a k-mer composition
# must spell out a solution to the String Reconstruction Problem.
print('Q4 -', 'True')


# Question 5:
# True or False: read breaking cannot transform reads with imperfect coverage into reads with perfect coverage.
print('Q5 -', 'False')