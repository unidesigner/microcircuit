import numpy as np
import networkx as nx

class Skeleton(object):

    def __init__(self):
        """
        Skeleton. Similar to a tree
        """
        pass

class Microcircuit(object):

    def __init__(self,
                 vertices,
                 connectivity,
                 vertices_properties = None,
                 connectivity_properties = None):
        """
        Microcircuit
        """
        self.vertices = vertices
        self.connectivity = connectivity
        self.vertices_properties = vertices_properties
        self.connectivity_properties = connectivity_properties

    def get_skeleton(self, id):
        """ Return skeleton as subgraph
        """
        # TODO: in what form? e.g. as microcircuit subgraph? (ensure no cycles)
        idx = np.where( self.connectivity_properties["id"]["data"] == id)[0]
        G = self.to_graph( add_attributes = True, use_identifier = False )
        return G.subgraph( idx )

    def to_graph(self, add_attributes = False, use_identifier = False):
        """ Return microcircuit as graph

        Parameters
        ----------
        add_attributes : bool
            Add spatial location and properties as attributes
            to nodes (vertices) and edges (connectivity)
        use_identifier : bool
            Use the `id` property as key for the graph
        """
        G = nx.DiGraph()
        if not use_identifier:
            G.add_edges_from( zip(self.connectivity[:,0], self.connectivity[:,1]) )
            if add_attributes:
                # add vertices attributes
                for idx, d in G.nodes_iter( data = True ):
                    d['location'] = self.vertices[idx,:]
                    for name, value in self.vertices_properties.items():
                        d[name] = value['data'][idx]
                # add connectivity attributes
                for idx,co in enumerate(self.connectivity):
                    for name, value in self.connectivity_properties.items():
                        G.edge[co[0]][co[1]][name] = value['data'][idx]
                    # compute euclidian length
                    G.edge[co[0]][co[1]]['length'] = np.linalg.norm( (self.vertices[co[1]]-self.vertices[co[0]]) )

        else:
            raise NotImplementedError()

        return G
