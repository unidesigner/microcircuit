

def set_weight(graph, edge_key):
    for u, v, d in graph.edges_iter(data=True):
        d['weight'] = d[edge_key]


def sum_edge_value(graph, edge_key):
    """ Sum edge value for a graph using `edge_key`
    """
    dist = 0.0
    for u, v, d in graph.edges_iter(data=True):
        dist += float(d[edge_key])
    # TODO: alternatives
    # - numpy sum on the array
    # - assume weight. graph.size( weighted = True )
    return dist


def compartmental_path_length(circuitgraph, metadata, attribute="type"):
    """ Return path length segregated by label type """
    ret = dict.fromkeys(metadata.keys(), 0.0)
    for u, v, d in circuitgraph.edges_iter(data=True):
        print d
        ret[d[attribute]] += float(d["length"])
    return ret
