import numpy as np
import networkx as nx
from IPython.utils import autoattr as desc

space_unit_conversion = {
    'nm' : 1, # nanometer
    'um' : 10 ** 3, # micrometer
    'mm' : 10 ** 6, # millimeter
    'cm' : 10 ** 7, # centimeter
    'm' : 10 ** 9 # meter
}

# The basic resolution
base_unit = 'nm'


class CircuitBase(object):

    def __init__(self,
                 vertices,
                 connectivity,
                 space_unit,
                 metadata = None,
                 vertices_properties = None,
                 connectivity_properties = None):

        if space_unit not in space_unit_conversion:
            raise ValueError('Invalid space unit %s, must be one of %s' %
                             (space_unit, space_unit_conversion.keys()))

        self.vertices = vertices
        self.connectivity = connectivity
        self.vertices_properties = vertices_properties
        self.connectivity_properties = connectivity_properties
                
        # Reverse metadata dictionary for additional information
        if metadata is None:
            self.metadata = {}
        else:
            self.metadata = metadata


class Circuit(CircuitBase):

    def __init__(self,
                 vertices,
                 connectivity,
                 space_unit = 'nm',
                 metadata = None,
                 vertices_properties = None,
                 connectivity_properties = None):
        """
        Circuit
        """
        CircuitBase.__init__(self,
                             vertices,
                             connectivity,
                             space_unit,
                             metadata,
                             vertices_properties,
                             connectivity_properties)

        # dictionary to map from index to id if it exists
        if self.vertices_properties.has_key( "id" ):
            a = self.vertices_properties["id"]["data"]
            self.relabel_verticesid = dict(zip(range(len(a)),a))
        else:
            self.relabel_verticesid = None

    @staticmethod
    def from_graph(self):
        pass

    def asgraph(self, add_attributes = False):
        """ Return circuit as graph

        Parameters
        ----------
        add_attributes : bool
            Add spatial location and properties as attributes
            to nodes (vertices) and edges (connectivity)
        """
        # TODO: directionality correct, bidirectional links, caching
        G = nx.DiGraph()
        G.add_edges_from( zip(self.connectivity[:,0], self.connectivity[:,1]) )

        if add_attributes:
            # TODO: Add metadata as graph attributes!
            
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

        return G
