
import sys
class Edge:
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


def calculate_max_path_to_node(cache, edges, start_node, node_label):
    """
    Cache will store max weight to each node and a string representation of the path to that node.
    """

    
    if not node_label in cache:
        # calc inbound path
        if node_label == start_node:
            # we're done
            cache[node_label] = (0, node_label)
        else:
            # calc maximal inbound path for this node. 
            # Init the list to large negative number to penalize nodes with no inbound edges. This is a nasty hack!
            all_inbound_weights = [((sys.maxsize * -1) + 1, '-')]           

            for edge in [e for e in edges if e.to_node == node_label]:
                max_inbound = calculate_max_path_to_node(cache, edges, start_node, edge.from_node)
                weight = edge.weight + max_inbound[0]
                all_inbound_weights.append((weight, max_inbound[1] + "->" + node_label))

            max = sys.maxsize * -1
            inbound = ()
            for temp in all_inbound_weights:
                if temp[0] > max:
                    max = temp[0]
                    inbound = temp

                cache[node_label] = inbound    
        
    return cache[node_label]


def main(argv=None):
    """
    :param argv: the command line args
    :return: nothing
    """
    if argv is None:
        argv = sys.argv

    start_node = "11"
    end_node = "27"

    all_edges = []

    all_edges_text = """a->b:5
a->c:6
a->d:5
b->c:2
b->f:4
c->e:4
c->f:3
c->g:5
d->e:4
d->f:5
e->g:2
f->g:1"""
    all_edges_lines = all_edges_text.strip(' ').split('\n')

    for line in all_edges_lines:
        from_to, weight = line.split(':')
        from_node, to_node = from_to.split('->')
        all_edges.append( Edge(from_node.strip(' '), to_node, int(weight)) )

    weight = calculate_max_path_to_node({}, all_edges, start_node, end_node)

    print(weight[0])
    print(weight[1])


if __name__ == "__main__":
    main()
    #sys.exit(main())
