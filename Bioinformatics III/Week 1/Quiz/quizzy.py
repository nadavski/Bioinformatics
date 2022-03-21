import numpy as np
import copy
import operator
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(operator.mul, range(n, n-r, -1))
    denom = reduce(operator.mul, range(1, r+1))
    return numer//denom
 

print('###############################################################################')
print('# Chapter 5 Quizz')
print('###############################################################################')

'''
There is a unique longest common subsequence of the strings TGTACG and GCTAGT. 
What is it?
'''
print('GTA')

'''
Imagine a hypothetical world in which there are two amino acids, X and Z, 
having respective masses 2 and 3. How many linear peptides can be formed 
from these amino acids having mass equal to 25? (Remember that the order of 
amino acids matters.)
'''
print(ncr(12,1) + ncr(11,3) + ncr(10,5) + ncr(9,7))

'''
Consider the following adjacency list of a DAG: 
a -> b: 3
a -> c: 6
a -> d: 5
b -> c: 2
b -> f: 4
c -> e: 4
c -> f: 3
c -> g: 7
d -> e: 4
d -> f: 5
e -> g: 2
f -> g: 1
What is the longest path in this graph? Give your answer as a 
sequence of nodes separated by spaces. 
(Note: a, b, c, d, e, f, g is a topological order for this graph.)
'''

class edge_weighted_graph:
    def __init__(self):
        # set of vertex
        self.vertex = set()
        # adjacency list of set of edge : 
        # key = vertex initial
        # value = ( ..., (vertex final, distance), ...)
        self.edge = {}
        return
        
    def add_edge(self, u, v, w):
        '''
        add a weigthed edge from vertex u to v
        '''
        assert u != v
        self.vertex.add(u)
        self.vertex.add(v)
        self.edge.setdefault(u,set()).add((v,w))
    
    def remove_edge(self, u, v, w):
        '''
        remove a weighted edge from vertex u to v
        '''
        assert u != v
        d = self.edge.get(u, set())
        d.remove((v, w))
    
    def sub_graph(self, u):
        '''
        return the sub graph starting from vertex u
        '''
        sg = edge_weighted_graph()
        on_stack = []
        on_stack.append(u)
        while (on_stack):
            u = on_stack.pop()
            for (v,w) in self.edge.get(u, set()):
                sg.add_edge(u, v, w)
                on_stack.append(v)
        return sg
    
    def reverse(self):
        '''
        return the reversed graph
        '''
        r = edge_weighted_graph()
        for u,d in self.edge.iteritems():
            for (v,w) in d:
                r.add_edge(v, u, w)
        return r
    
    def sort(self):
        '''
        return a topologically sorted list of vertex
        '''
        s = []
        g = copy.deepcopy(self)
        r = g.reverse()
        candidates = [ u for u in self.vertex if not r.edge.get(u, set())]
        while candidates:
            u = candidates.pop()
#            print '---------'
#            print 'u=',u
#            print 'g.edge',g.edge
#            print 'r.edge',r.edge
            s.append(u)
            for (v,w) in set(g.edge.get(u, set())):
                # remove u->v edge from g and u-> from r
                g.remove_edge(u, v, w)
                r.remove_edge(v, u, w)
                if not r.edge[v]:
                    r.edge.pop(v, None)
                    candidates.append(v)
            g.edge.pop(u, None)
        assert not g.edge
        assert not r.edge
        return s
    
    def __str__(self):
        s = ''
        for u,d in self.edge.iteritems():
            for (v,w) in d:
                 s += str(u) + '->' + str(v) + ':' + str(w) + '\n'
        return s


def dag_longest_path(source, sink, edges):
    '''
    Input: 
    the source node of a graph, 
    the sink node of the graph,
    followed by a list of edges in the graph.    
    Output: longest path from source to sink as a the list of nodes.
    '''
    g = edge_weighted_graph()
    for (u,v,w) in edges:
        g.add_edge(u, v, w)
    g = g.sub_graph(source)
    order = g.sort()

edge = (('a','b',3),('a','c',6),('a','d',5),('b','c',2),('b','f',4),('c','e',4),('c','f',3),('c','g',7),('d','e',4),('d','f',5),('e','g',2),('f','g',1))
for source in 'abcdefg':
    for sink in 'abcdefg':
        if (source < sink):
            print(dag_longest_path(source,sink,edge))
            
            