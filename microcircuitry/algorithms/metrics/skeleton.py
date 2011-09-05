import numpy as np

def total_path_length( skeleton ):
    return sum_edge_value( skeleton, edge_key = 'distance' )

def set_weight( graph, edge_key ):
    for u,v,d in graph.edges_iter( data = True ):
        d['weight'] = d[edge_key]
        
def sum_edge_value( graph, edge_key ):
    """ Sum edge value for a graph
    """
    dist = 0.0
    for u,v,d in graph.edges_iter( data = True ):
        dist += float(d[edge_key])
    # TODO: alternatives
    # - numpy sum on the array
    # - assume weight. graph.size( weighted = True )
    return dist