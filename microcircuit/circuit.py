import numpy as np
import networkx as nx

import constants as const


class CircuitBase(object):

    def __init__(self,
                 vertices, connectivity, space_unit,
                 metadata=None, vertices_properties=None,
                 connectivity_properties=None):
        if space_unit not in const.space_unit_conversion:
            raise ValueError('Invalid space unit %s, must be one of %s' %
                             (space_unit,
                              constants.space_unit_conversion.keys()))
        self.vertices = vertices
        self.connectivity = connectivity
        self.vertices_properties = vertices_properties
        self.connectivity_properties = connectivity_properties
        # Reverse metadata dictionary for additional information
        if metadata is None:
            self.metadata = {}
        else:
            self.metadata = metadata

    def get_vertices_property(self, key, metadata=False):
        """Get vertices property
        """
        if key in self.vertices_properties:
            if metadata:
                return (self.vertices_properties[key][const.DATA],
                        self.vertices_properties[key][const.METADATA])
            else:
                return self.vertices_properties[key][const.DATA]
        else:
            raise Exception("No vertices property {0} exists.".format(key))

    def get_connectivity_property(self, key, metadata=False):
        """Get connectivity property

        Parameters
        ----------
        key : str
            The property name to retrieve
        metadata : bool
            If True, returns a tuple with (array,metadata)

        Returns
        -------
        prop_array : `array_like`
        """
        if key in self.connectivity_properties:
            if metadata:
                return (self.connectivity_properties[key][const.DATA],
                        self.connectivity_properties[key][const.METADATA])
            else:
                return self.connectivity_properties[key][const.DATA]

        else:
            raise Exception("No connectivity property {0} exists.".format(key))


class Circuit(CircuitBase):

    def __init__(self, vertices, connectivity,
                 space_unit='nm', metadata=None,
                 vertices_properties=None, connectivity_properties=None):
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

        # map from vertices identifiers to indices
        self.map_vertices_id2index = dict(zip(vertices,range(len(vertices))))

    def asgraph(self, add_attributes=False):
        """ Return circuit as graph

        Parameters
        ----------
        add_attributes : bool
            Add spatial location and properties as attributes
            to nodes (vertices) and edges (connectivity)

        Returns
        -------
        G : NetworkX DiGraph
        """
        # TODO: directionality correct, bidirectional links, caching
        # The interpretation whether a connector is implicitly
        # directional (e.g. chemical synapses) or bidirectional (gap junctions)
        # is made when extracting a connectome from the circuit
        G = nx.DiGraph()
        G.add_edges_from(
            zip(self.connectivity[:, 0], self.connectivity[:, 1]))
        if add_attributes:
            G.graph = self.metadata
            location = self.get_vertices_property(const.LOCATION)
            # add vertices attributes
            for id, d in G.nodes_iter(data=True):
                idx=self.map_vertices_id2index[id]
                d['location'] = location[idx, :]
                for name, value in self.vertices_properties.items():
                    if const.LOCATION == name:
                        continue
                    d[name] = value['data'][idx]
            # add connectivity attributes
            for idx, co in enumerate(self.connectivity):
                s,e=self.map_vertices_id2index[co[0]],self.map_vertices_id2index[co[1]]
                for name, value in self.connectivity_properties.items():
                    G.edge[co[0]][co[1]][name] = value['data'][idx]
                # compute euclidian length
                G.edge[co[0]][co[1]]['length'] = np.linalg.norm(
                        (location[e] - location[s]))
        return G
