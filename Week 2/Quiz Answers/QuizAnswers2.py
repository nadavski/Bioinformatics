def pathToGenome(path):
    geno = ''
    for seq in path:
        geno += seq[0]
    return geno + seq[1:]


def stringSpellByGapPat(patterns, k, d):

    init = []
    term = []
    for pattern in patterns:
        fst, lst = pattern.split('|')
        init.append(fst)
        term.append(lst)
    init = pathToGenome(init)
    term = pathToGenome(term)
    for i in range(k + d + 1, len(init)):
        if init[i]  != term[i-k-d]:
            return "None"
    return init + term[-(k+d):]

def DBFromRP(Patterns, k):
    '''
    De Bruijn Graph from Paired Read (k + d + k) k-mers
    Construct the De Bruijn graph adjacency list from a collection of paried read k-mers.
    
    Args:
        Patterns (list[string]): Collection of paried read k-mers used to construct the graph.
        k (int): Length of kmers in read pairs.
        
    Returns:
        dict[string] = list[string]: Adjacency list of the De Bruijn graph resulting from reads.
    '''
    kDict = dict()
    for pattern in Patterns:
        r1, r2 = pattern.split('|')
        fst = f"{r1[:k]}|{r2[:k]}"
        lst = f"{r1[-k:]}|{r2[-k:]}"
        if fst not in kDict:
            kDict[fst] = [lst]
        else:
            kDict[fst].append(lst)
    return kDict

import random as rd
from collections import deque
def graphListToDict(gList):
    '''
    Transform an adjacency list into a dictionary of nodes and out edges.
    
    Args:
        gList (list[string]): List of nodes and out edges in a single line format [node -> edge1,edge2,etc..]
    
    Returns:
        dict[string] = list[string]: Mapping of nodes to list of out edges.
    '''
    gList = [x.strip().split(' ') for x in gList]
    gDict = dict()
    for row in gList:
        gDict[row[0]] = row[2].split(',')
    return gDict

def followTrail(start, graph):
    '''
    Given a start node, randomly traverse through graph on unused edges.
    
    Args:
        start (string): First node to begin eulerian walk.
        graph (dict[string] = list[string]): Graph to traverse.
        
    Returns:
        list[string]: A random path from start traversing unused edges until none avalibale. 
    '''
    res = []
    pos = start
    while pos:
        res.append(pos)
        if pos not in graph:
            pos = False
        else:
            pos = rd.choice(graph[pos])
            graph[res[-1]].remove(pos)
        if res[-1] in graph and len(graph[res[-1]]) == 0:
            graph.pop(res[-1], None)
    return res


def eulerianCycle(graph, start=None, ret=True, prnt=False, output=None):
    '''
    Eulerian Cycle
    Determine a Eulerian Cycle within a given graph.
    
    Args:
        graph (dict[string] = list[string]): Graph to find a Eulerian path within.
        start (string, optional): Defualts to None. If set starts to find cycle at specified node.
        ret (bool, optional): Defaults to True. Returns list of cycle.
        prnt (bool, optional): Defualts to False. Prints formatted cycle if True.
        output (string, optional): Defualts to None. If not None, resulting cycle is written to the given filename.
        
    Returns:
        list[string], optional: List of the found Eulerian cycle. 
    '''
    Q = deque()
    if start == None:
        start = rd.choice(list(graph.keys()))
    Stak = deque(followTrail(start, graph))
    while Stak:
        t = Stak.pop()
        if t not in graph:
            Q.appendleft(t)
        else:
            Stak.extend(followTrail(t, graph))
    
    if prnt or output != None:
        if prnt:
            print(*list(Q), sep='->')
        if output != None:
            f = open(output, 'w')
            for i, nd in enumerate(list(Q)):
                if i != 0:
                    f.write("->")
                f.write(nd)
            f.write("\n")
            f.close()
    if ret:
        return list(Q)


def calcInOut(graph):
    '''
    For a given graph calculate the in and out degrees for each node.
    
    Args:
        graph (dict[string] = list[string]): Mapping representing a graph and associated out edges.
        
    Returns:
        dict[string] = (dict[string] = int): Mapping of a node to its in and out degrees
            dict[node] = {'in': X, 'out': X}
    '''
    ioCount = dict()
    for node in graph:
        if node not in ioCount:
            ioCount[node] = {'in': 0, 'out': len(graph[node])}
        for n in graph[node]:
            if n not in ioCount:
                if n in graph:
                    ioCount[n] = {'in': 1, 'out': len(graph[n])}
                else:
                    ioCount[n] = {'in': 1, 'out': 0}
            else:
                ioCount[n]['in'] += 1
    return ioCount

def eulerianPath(graph, ret=True, prnt=False, output=None):
    '''
    Find Eulerian Path through a graph.
    
    Args:
        graph (dict[string] = list[string]): Graph to find a Eulerian path within.
        ret (bool, optional): Defaults to True. Returns list of path.
        prnt (bool, optional): Defualts to False. Prints formatted path if True.
        output (string, optional): Defualts to None. If not None, resulting path is written to the given filename.
        
    Returns:
        list[string], optional: List of the found Eulerian path. 
    '''
    ioCount = calcInOut(graph)
    strt = rd.choice(list(graph.keys()))
    for key in graph:
        if key not in ioCount or ioCount[key]['out'] - ioCount[key]['in'] == 1:
            strt = key
    path = eulerianCycle(graph, start=strt)
            
    if prnt or output != None:
        if prnt:
            print(*path, sep='->')
        if output != None:
            f = open(output, 'w')
            for i, nd in enumerate(path):
                if i != 0:
                    f.write("->")
                f.write(nd)
            f.close()
    if ret:
        return path


def strReconsructFromRP(pairs, k, d):
    '''
    Reconstruct a string from a collection of paried reads
    Builds the De Bruijn graph, finds a eulerian path, and attempts string reconstruction from found path.
    
    Args:
        pairs (list[string]): Collection of (k ,d)-mers representing paired reads.
        k (int): Length of each k-mer in a paried read.
        d (int): Distance between gapped reads.
        
    Returns:
        string: Resulting string reconstruction from collection of (k, d)-mers if possible.
    '''
    db = DBFromRP(pairs, k-1)
    path = eulerianPath(db)
    st = stringSpellByGapPat(path, k, d)
    return st

with open("dataset_204_16.txt") as inFile:
    data = inFile.readlines()

k, d = data[0].strip().split(' ')
pat = []
for i in range(1, len(data)):
    pat.append(data[i].strip())
strReconsructFromRP(pat, int(k), int(d))


pat2 = ['ACC|ATA',
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

print(strReconsructFromRP(pat2, 3, 1))