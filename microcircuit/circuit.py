import numpy as np
import networkx as nx
import h5py

import constants as const

DEBUG = False

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
        for k,v in outconnectors.items():
            for skid in v['target_skeleton_ids']:
                if skid in skeletons:
                    skeletons[skid]['synaptic_count'] += 1
                else:
                    skeletons[skid] = dict.fromkeys(['synaptic_count'],1)
        return skeletons

    def get_upstream_skeletons(self):
        """ Return upstream skeleton ids and number of connectors
        """
        inconnectors = self.get_incoming_connector_nodes()
        skeletons = {}
        for k,v in inconnectors.items():
            for skid in v['source_skeleton_ids']:
                if skid in skeletons:
                    skeletons[skid]['synaptic_count'] += 1
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

    def get_subgraph(self, skeleton_ids):
        """ Returns a directed NetworkX subgraph
        """
        g = nx.DiGraph()
        skeletons = {}
        for skid in skeleton_ids:
            skeletons[skid] = self.get_skeleton( skid )
            g.add_node( skid, {'number_of_nodes': skeletons[skid].number_of_nodes(),
                               'total_length': skeletons[skid].get_total_length(),
                               'neuron_name': skeletons[skid].get_neuron_name() } )
        # add connectivity
        for skid, skeleton in skeletons.items():
            down_skeletons = skeleton.get_downstream_skeletons()
            for downid, d in down_skeletons.items():
                # only add edge for skeleton in target set
                if downid in skeleton_ids:
                    g.add_edge( skid, downid, {'synaptic_count': d['synaptic_count'] })

            up_skeletons = skeleton.get_upstream_skeletons()
            for upid, d in up_skeletons.items():
                # only add edge for skeleton in target set
                if upid in skeleton_ids:
                    g.add_edge( upid, skid, {'synaptic_count': d['synaptic_count'] })

        return g

    def get_fos_microcircuit(self, skeleton_id, scale_factor = 1.):
        """ Returns a fos microcircuit actor

        Parameters
        ----------
        scale_factor : float
            Divide the vertices coordinates by this factor
        """
        conidx = np.where(self.connectivity_properties['skeletonid']['data']==skeleton_id)[0]

        # connectivity
        connectivity_id = self.connectivity[conidx]
        if DEBUG:
            print 'connectivity id', connectivity_id, connectivity_id.shape

        # map to new index based array
        connectivity_indices = np.zeros( connectivity_id.shape, dtype=np.uint32 )
        for i,c in enumerate(connectivity_id):
            connectivity_indices[i,0]=self.map_vertices_id2index[connectivity_id[i,0]]
            connectivity_indices[i,1]=self.map_vertices_id2index[connectivity_id[i,1]]
        if DEBUG:
            print 'connectivity indices', connectivity_indices, connectivity_indices.shape

        connectivity_type = self.connectivity_properties['type']['data'][conidx]
        if DEBUG:
            print 'connectivity type', connectivity_type, connectivity_type.shape

        vertices_location = self.vertices_properties['location']['data'][ connectivity_indices.ravel() ].astype(np.float32) / scale_factor
        if DEBUG:
            print 'vertices_location', vertices_location, vertices_location.shape

        # connectivity is now simplified to the reduced array
        connectivity_skeleton_with_synapse = np.array( range(len(vertices_location)), dtype = np.uint32 )
        connectivity_skeleton_with_synapse = connectivity_skeleton_with_synapse.reshape( (len(connectivity_skeleton_with_synapse)/2, 2) )
        if DEBUG:
            print 'connectivity_skeleton_with_synapse', connectivity_skeleton_with_synapse, connectivity_skeleton_with_synapse.shape

        connectivity_skeletonid = skeleton_id * np.ones( connectivity_type.shape, dtype = np.uint32 )
        miin = connectivity_skeletonid.min()
        if DEBUG:
            print 'connectivity skeletonid', connectivity_skeletonid, connectivity_skeletonid.shape

        return skeleton_id, vertices_location, connectivity_skeleton_with_synapse, connectivity_skeletonid, miin, connectivity_type

    def get_skeleton_allnames(self, skeleton_id ):
        strname_idx = np.where(self.metadata['skeleton_name']['data']['skeletonid']==skeleton_id)[0][0]
        strname = self.metadata['skeleton_name']['data']['name'][strname_idx]
        return strname.split('|')

    def get_skeleton_number_of_nodes(self, skeleton_id ):
        return len(np.where(self.vertices_properties['skeletonid']['data']==skeleton_id)[0])

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
                    'userid': self.vertices_properties['userid']['data'][vertex_index],
                    'creation_time': self.vertices_properties['creation_time']['data'][vertex_index],
                    'modification_time': self.vertices_properties['modification_time']['data'][vertex_index]
                })

            # add connectivity properties
            for i in conidx:
                from_id = self.connectivity[i,0]
                to_id = self.connectivity[i,1]

                g.edge[from_id][to_id]['type'] = typedict[self.connectivity_properties['type']['data'][i]]
                dist = np.abs( g.node[to_id]['location'] - g.node[from_id]['location'] )
                g.edge[from_id][to_id]['length'] = np.linalg.norm( dist )

                dist = np.abs( g.node[to_id]['creation_time'] - g.node[from_id]['creation_time'] )
                g.edge[from_id][to_id]['delta_creation_time'] = np.linalg.norm( dist )

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


