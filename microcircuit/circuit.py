import numpy as np
import networkx as nx
import h5py

import constants as const


class CircuitBase(object):

    def __init__(self, space_unit='nm'):
        if space_unit not in const.space_unit_conversion:
            raise ValueError('Invalid space unit %s, must be one of %s' %
                             (space_unit,
                              constants.space_unit_conversion.keys()))
        self.vertices = None
        self.connectivity = None
        self.vertices_properties = {}
        self.connectivity_properties = {}
        self.metadata = {}
        self.map_vertices_id2index = {}
        self.space_unit = space_unit

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


class Skeleton(object):

    def __init__(self, id, allnames, graph):
        self.id = id
        self.allnames = allnames
        self.graph = graph

    def number_of_nodes(self):
        """ Returns the number of treenodes and connector nodes
        of the skeleton
        """
        return self.graph.number_of_nodes()

    def get_downstream_skeletons(self):
        """ Return downstream skeleton ids and number of connectors
        """
        outconnectors = self.get_outgoing_connector_nodes()
        skeletons = {}
        for k,v in outconnectors:
            for skid in v['target_skeleton_ids']:
                if skid in skeletons:
                    skeletons['synaptic_count'] += 1
                else:
                    skeletons[skid] = dict.fromkeys(['synaptic_count'],1)
        return skeletons

    def get_upstream_skeletons(self):
        """ Return upstream skeleton ids and number of connectors
        """
        inconnectors = self.get_incoming_connector_nodes()
        skeletons = {}
        for k,v in inconnectors:
            for skid in v['source_skeleton_ids']:
                if skid in skeletons:
                    skeletons['synaptic_count'] += 1
                else:
                    skeletons[skid] = dict.fromkeys(['synaptic_count'],1)
        return skeletons

    def get_outgoing_connector_nodes(self):
        """ Returns a dictionary keyed by connector node id and
        their associated data like a list of target skeleton ids
        """
        incoming = {}
        for u, v, d in self.graph.edges_iter(data=True):
            if d['type'] == 'presynaptic_to':
                incoming[v] = self.graph.node[v]
        return incoming

    def get_incoming_connector_nodes(self):
        """ Returns a dictionary keyed by connector node id and
        their associated data like a list of the incoming skeleton id
        """
        incoming = {}
        for u, v, d in self.graph.edges_iter(data=True):
            if d['type'] == 'postsynaptic_to':
                incoming[v] = self.graph.node[v]
        return incoming

    def get_neuron_name(self):
        """ Returns the last string of the allnames list
        """
        return self.allnames[-1]

    def get_total_length(self):
        """ Sum over all the segment lengths
        """
        dist = 0.0
        for u, v, d in self.graph.edges_iter(data=True):
            dist += float(d['length'])
        return dist


class Circuit(CircuitBase):

    def __init__(self):
        """ Initialize a neural circuit
        """
        CircuitBase.__init__(self)

    def _remap_vertices_id2indices(self):
        # map from vertices identifiers to indices
        self.map_vertices_id2index = dict(zip(self.vertices,range(len(self.vertices))))

    def get_all_skeletons(self):
        """ Returns a list of all skeleton ids
        """
        # TODO: len should be equal to metadata entry
        return list(np.unique(self.connectivity_properties['skeletonid']['data']))

    def get_skeleton(self, skeleton_id ):
        """ Return skeleton object
        """
        # TODO: is the skeletonid found at all in this circuit?

        # extract allname
        strname_idx = np.where(self.metadata['skeleton_name']['data']['skeletonid']==skeleton_id)[0][0]
        strname = self.metadata['skeleton_name']['data']['name'][strname_idx]
        extracted_names = strname.split('|')

        # extract skeleton as graph including pre/post synapses to connectors

        # extract connectivity ids
        conidx = np.where(self.connectivity_properties['skeletonid']['data']==skeleton_id)[0]

        # if none found using the connectivity property, this may happen for skeletons
        # with a single treenode, so look up the skeletonid as a vertex property
        if not len(conidx):
            conidx = None
            if self.connectivity_properties.has_key('skeletonid'):
                vertidx = np.where(self.connectivity_properties['skeletonid']['data']==skeleton_id)[0]
                if not len(vertidx):
                    raise Exception('Invalid NeuroHDF. Skeleton with id {0} has no associated data'.format(skeleton_id))
            print 'debug: vertidx', vertidx
        else:
            pass
            #print 'debug: conidx', conidx

        g = nx.DiGraph()
        if len(conidx):
            g.add_edges_from( zip(self.connectivity[conidx, 0], self.connectivity[conidx, 1]) )

            # FIXME: there seems to be an issue when converting the name to string
            # http://code.google.com/p/h5py/issues/detail?id=217

            # get type metadata
            typemeta = self.connectivity_properties['type']['metadata']
            typevals = typemeta['value_name']['value']
            typename = typemeta['value_name']['name']
            typedict = {}
            for i,k in enumerate(typevals):
                typedict[typevals[i]] = typename[i]
            inv_typedict = dict((v,k) for k, v in typedict.iteritems())
            print typedict, inv_typedict['postsynaptic_to']
            verttypemeta = self.vertices_properties['type']['metadata']
            verttypevals = verttypemeta['value_name']['value']
            verttypename = verttypemeta['value_name']['name']
            verttypedict = {}
            for i,k in enumerate(verttypevals):
                verttypedict[verttypevals[i]] = verttypename[i]

            vertices_unique = np.unique(self.connectivity[conidx,:])
            for id in vertices_unique:
                vertex_index = self.map_vertices_id2index[id]
                g.add_node( id, {
                    'location': self.vertices_properties['location']['data'][vertex_index,:],
                    'type': verttypedict[self.vertices_properties['type']['data'][vertex_index]],
                    'confidence': self.vertices_properties['confidence']['data'][vertex_index],
                    'radius': self.vertices_properties['radius']['data'][vertex_index],
                    'userid': self.vertices_properties['userid']['data'][vertex_index]
                })

            # add connectivity properties
            for i in conidx:
                from_id = self.connectivity[i,0]
                to_id = self.connectivity[i,1]

                g.edge[from_id][to_id]['type'] = typedict[self.connectivity_properties['type']['data'][i]]
                dist = np.abs( g.node[to_id]['location'] - g.node[from_id]['location'] )
                g.edge[from_id][to_id]['length'] = np.linalg.norm( dist )

                #print typedict[self.connectivity_properties['type']['data'][i]]
                if typedict[self.connectivity_properties['type']['data'][i]] == 'presynaptic_to':
                    # It's a feature, not a bug: This does discard single
                    # node skeletons!
                    target_conn_indices = np.where( (self.connectivity[:,1] == to_id) & \
                            (self.connectivity_properties['type']['data'] == inv_typedict['postsynaptic_to']) )[0]
                    targetnodes = self.connectivity[target_conn_indices,0]
                    target_skeleton_list = []
                    for nid in targetnodes:
                        target_skeleton_list.append( self.connectivity_properties['skeletonid']['data'][self.map_vertices_id2index[nid]] )
                    g.node[to_id]['target_skeleton_ids'] = target_skeleton_list
                    g.node[to_id]['target_node_ids'] = targetnodes
                elif typedict[self.connectivity_properties['type']['data'][i]] == 'postsynaptic_to':
                    source_conn_indices = np.where( (self.connectivity[:,1] == to_id) &\
                            (self.connectivity_properties['type']['data'] == inv_typedict['presynaptic_to']))[0]
                    sourcenodes = self.connectivity[source_conn_indices,0]
                    source_skeleton_list = []
                    for nid in sourcenodes:
                        source_skeleton_list.append( self.connectivity_properties['skeletonid']['data'][self.map_vertices_id2index[nid]] )
                    g.node[to_id]['source_skeleton_ids'] = source_skeleton_list
                    g.node[to_id]['source_node_ids'] = sourcenodes

        else:
            if vertidx:
                pass

        return Skeleton(
            id = skeleton_id,
            allnames = extracted_names,
            graph = g )


def load_neurohdf(filename, hdf5path, memmapped=False):
    """ Loads the circuit from a NeuroHDF file as exported from CATMAID

    Parameters
    ----------
    filename : str
        Path to the NeuroHDF file
    hdfpath : str
        HDF5 path to the irregular dataset containing the circuit
        e.g. /Microcircuit
    """
    if memmapped:
        raise NotImplementedError('Memmapped HDF5 reading not yet implemented')

    circuit = Circuit()

    f = h5py.File(filename, 'r')
    circuitdata_group=f[hdf5path]
    vertices_group = circuitdata_group.get('vertices')
    connectivity_group = circuitdata_group.get('connectivity')
    metadata_group = circuitdata_group.get('metadata')

    def helpdict(v):
        helpdict = dict.fromkeys( v.attrs.keys() )
        for k in helpdict:
            helpdict[k] = v.attrs.get(k)
        return helpdict

    for k,v in vertices_group.items():
        if k == 'id':
            circuit.vertices = vertices_group[k].value
        else:
            circuit.vertices_properties[k] = dict.fromkeys( [const.DATA, const.METADATA] )
            circuit.vertices_properties[k][const.DATA] = v.value
            circuit.vertices_properties[k][const.METADATA] = helpdict(v)
        print('Added vertices {0}'.format(k))

    for k,v in connectivity_group.items():
        if k == 'id':
            circuit.connectivity = connectivity_group[k].value
        else:
            circuit.connectivity_properties[k] = dict.fromkeys( [const.DATA, const.METADATA] )
            circuit.connectivity_properties[k][const.DATA] = v.value
            circuit.connectivity_properties[k][const.METADATA] = helpdict(v)

        print('Added connectivity {0}'.format(k))
    if metadata_group:
        for k,v in metadata_group.items():
            circuit.metadata[k] = dict.fromkeys( [const.DATA, const.METADATA] )
            circuit.metadata[k][const.DATA] = v.value
            circuit.metadata[k][const.METADATA] = helpdict(v)
        print('Added metadata {0}'.format(k))
    circuit._remap_vertices_id2indices()
    f.close()

    return circuit