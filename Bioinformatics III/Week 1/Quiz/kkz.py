

import copy 


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
    assert source in order
    assert sink in order
    if (not sink in order) or (not source in order):
        return None

    a = order.index(source)
    b = order.index(sink)
    if (a >= b):
        return None
#    assert a < b
    assert sink in order
    # order contains the topological order of graph
    order = order[a+1:b+1]
    # path from-to source is of len 0
    s = {source:0}
    bt = {source:None}
    # get the incoming the edges
    r = g.reverse()
    # compute the max path len along the topological order 
    # from source and until sink is met
    for u in order:
        lmax = float('-Inf')
        for (v,w) in r.edge[u]:            
            l = s[v]+w
            if (l > lmax):
                lmax = l
                s[u] = l
                bt[u] = v
    # backtrack the longest path
    u = order[-1]
    path = []
    while (not u is None):
        path.append(u)
        u = bt[u] 
    path.reverse()
    return s[sink],path
    
#assert dag_longest_path(0,4,((0,1,7),(0,2,4),(2,3,2),(1,4,1),(3,4,3))) == (9, [0, 2, 3, 4])


#source = int(lines[0])
#sink = int(lines[1])
#edges = map(parse, lines[2:])

edge = (('a','b',3),('a','c',6),('a','d',5),('b','c',2),('b','f',4),('c','e',4),('c','f',3),('c','g',7),('d','e',4),('d','f',5),('e','g',2),('f','g',1))
for source in 'abcdefg':
    for sink in 'abcdefg':
        if (source < sink):
            print(dag_longest_path(source,sink,edge))



