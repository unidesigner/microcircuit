# Needs refactoring

import networkx as nx
import numpy as np

from microcircuit.utils import extract_value_customdict
import constants as const

class Connectome(object):

    def __init__(self, metadata=None, circuit=None, graph=None):
        """Connectome or Wiring Diagram. Represents a graph view on a `Circuit`
        """

        # includes neuronmap that maps neuron/skeletonid to label etc.
        self.metadata = metadata

        # the base Circuit that used to construct this connectome
        self.circuit = circuit

        if not circuit is None:
            # dictionary of skeleton objects keyed by their id
            self.skeletons = self.get_skeleton_dict()
            # NetworkX graph with nodes (skeletons) and edges (connectivity)
            self.graph = self.get_network_connectivity()
        else:
            self.skeletons = None
            self.graph = graph

    def set_circuit(self, metadata=None, circuit=None):
        """ Set a new circuit for the connectome object
        """
        if circuit is None:
            return
        else:
            self.circuit = circuit

        if not metadata is None:
            self.metadata = metadata

        # update the graph and skeletons
        self.skeletons = self.get_skeleton_dict()
        self.graph = self.get_network_connectivity()
            

    def get_network_connectivity(self):
        """Extract a network from the input circuit where
        nodes are skeletons and edges are the number of synaptic
        connections
        """
        if self.circuit is None:
            return None

        #metc = self.circuit.get_vertices_property(const.TYPE, True)[1]
        mecotc = self.circuit.get_connectivity_property(const.TYPE, True)[1]

        #vertices_type = self.circuit.get_vertices_property(const.TYPE)
        # can select pre, post, gap
        connectivity_type = self.circuit.get_connectivity_property(const.TYPE)
        connectivity_skeletonid = self.circuit.get_connectivity_property(const.SKELETON_ID)

        # define valid transform of M:N connector pairs and whether directional
        # not directional implies bidirectional
        chemical_synapse = (const.PRESYNAPTIC, const.POSTSYNAPTIC, True)

        presynaptic_value = extract_value_customdict(mecotc,chemical_synapse[0])
        postsynaptic_value = extract_value_customdict(mecotc,chemical_synapse[1])
        gap_junction = extract_value_customdict(mecotc,const.GAP_JUNCTION)

        connector_connectivity_pre_idx = np.where((connectivity_type == presynaptic_value))[0]
        connector_connectivity_post_idx = np.where((connectivity_type == postsynaptic_value))[0]

        gap_idx = np.where((connectivity_type == gap_junction))
        if len(gap_idx)==0:
            connector_connectivity_gap_idx = []
        else:
            connector_connectivity_gap_idx = gap_idx[0]

        # {connid : {'pre': [preskelid1, preskelid2], 'post': [postskelid1, postskelid2]}}

        ds = {}
        for idx in connector_connectivity_pre_idx:
            preidx, conidx = self.circuit.connectivity[idx]
            skeletonid = connectivity_skeletonid[idx]
            if ds.has_key(conidx):
                if ds[conidx].has_key(const.PRESYNAPTIC):
                    ds[conidx][const.PRESYNAPTIC].append( skeletonid )
            else:
                ds[conidx] = {}
                ds[conidx][const.PRESYNAPTIC] = [skeletonid]

        for idx in connector_connectivity_post_idx:
            # assume correct directionality
            conidx, postidx = self.circuit.connectivity[idx]
            skeletonid = connectivity_skeletonid[idx]
            if ds.has_key(conidx):
                if ds[conidx].has_key(const.POSTSYNAPTIC):
                    ds[conidx][const.POSTSYNAPTIC].append( skeletonid )
                else:
                    ds[conidx][const.POSTSYNAPTIC] = [skeletonid]
            else:
                ds[conidx] = {}
                ds[conidx][const.POSTSYNAPTIC] = [skeletonid]

        # add gap junctions
        for idx in connector_connectivity_gap_idx:
            gapidx, conidx = self.circuit.connectivity[idx]
            skeletonid = connectivity_skeletonid[idx]
            if ds.has_key(conidx):
                if ds[conidx].has_key(const.GAP_JUNCTION):
                    ds[conidx][const.GAP_JUNCTION].append( skeletonid )
                else:
                    ds[conidx][const.GAP_JUNCTION] = [skeletonid]
            else:
                ds[conidx] = {}
                ds[conidx][const.GAP_JUNCTION] = [skeletonid]

        # build graph
        G = nx.DiGraph()
        G.add_nodes_from(np.unique(connectivity_skeletonid))
        for k,v in ds.items():
            # only loop when both pre and post exist
            if v.has_key(const.PRESYNAPTIC) and v.has_key(const.POSTSYNAPTIC):
                for preskelid in v[const.PRESYNAPTIC]:
                    for postkelid in v[const.POSTSYNAPTIC]:
                        if G.has_edge(preskelid, postkelid):
                            G.edge[preskelid][postkelid][const.CONNECTOME_CHEMICAL_SYNAPSE] += 1
                        else:
                            G.add_edge(preskelid, postkelid, {const.CONNECTOME_CHEMICAL_SYNAPSE: 1})
                            
            # all-to-all for gap junctions (usually only two, if more, log)
            if v.has_key(const.GAP_JUNCTION):
                print 'gapjunct', v[const.GAP_JUNCTION]
                if len(v[const.GAP_JUNCTION]) > 2:
                    print("Gap junction with more than two partners found. Not counted.")
                    continue
                if len(v[const.GAP_JUNCTION]) < 2:
                    print("Gap junction with less than two partners found. Not counted.")
                    continue

                preskelid = v[const.GAP_JUNCTION][0]
                postskelid = v[const.GAP_JUNCTION][1]

                # no self-loops
                if preskelid == postskelid:
                    continue
                # because we are adding to a DiGraph, we need to check both ways
                # need to be bidirectional (symmetrical)

                G.add_edge(preskelid, postskelid)
                G.add_edge(postskelid, preskelid)

                if G.edge[preskelid][postskelid].has_key(const.CONNECTOME_ELECTRICAL_SYNAPSE):
                    # already existing electrical synapse, add this one
                    G.edge[preskelid][postskelid][const.CONNECTOME_ELECTRICAL_SYNAPSE] += 1
                else:
                    G.edge[preskelid][postskelid][const.CONNECTOME_ELECTRICAL_SYNAPSE] = 1

                if G.edge[postskelid][preskelid].has_key(const.CONNECTOME_ELECTRICAL_SYNAPSE):
                    # already existing electrical synapse, add this one
                    G.edge[postskelid][preskelid][const.CONNECTOME_ELECTRICAL_SYNAPSE] += 1
                else:
                    # no existing electrical synapse, so we need to add the key
                    G.edge[postskelid][preskelid][const.CONNECTOME_ELECTRICAL_SYNAPSE] = 1
        return G

    def get_skeleton_dict(self):
        """ Return dictionary keyed by skeleton id containing as value
        the skeletons as subgraph structure
        """
        # retrieve unique identifiers of skeletons
        if self.circuit is None:
            return None

        uniqueidarr = np.unique(
            self.circuit.get_connectivity_property(const.SKELETON_ID))

        graph = self.circuit.asgraph(add_attributes=True)

        if not uniqueidarr is None:
            # for each skeleton, use id as dictionary key
            skeletons = dict.fromkeys(uniqueidarr)
            # for each skeleton id, retrieve connectivity indices
            idarr = self.circuit.connectivity_properties[const.SKELETON_ID][const.DATA]
            for id in uniqueidarr:
                # compute list of indices for each identifier
                idx = np.where(idarr == id)[0]
                # store each skeleton as subgraph
                skeletons[id] = graph.subgraph(idx)
        else:
            raise Exception("No unique skeleton identifiers found")

        return skeletons
