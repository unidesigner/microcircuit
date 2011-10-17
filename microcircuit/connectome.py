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

    def get_network_connectivity(self):
        """Extract a network from the input circuit where
        nodes are skeletons and edges are the number of synaptic
        connections
        """
        metc = self.circuit.get_vertices_property(const.TYPE, True)[1]
        mecotc = self.circuit.get_connectivity_property(const.TYPE, True)[1]

        vertices_type = self.circuit.get_vertices_property(const.TYPE)
        # can select pre, post, gap
        connectivity_type = self.circuit.get_connectivity_property(const.TYPE)
        connectivity_skeletonid = self.circuit.get_connectivity_property(const.SKELETON_ID)

        # define valid transform of M:N connector pairs and whether directional
        # not directional implies bidirectional
        chemical_synapse = (const.PRESYNAPTIC, const.POSTSYNAPTIC, True)
        gap_junctions = (const.GAP_JUNCTION, const.GAP_JUNCTION, False)

        presynaptic_value = extract_value_customdict(mecotc,chemical_synapse[0])
        postsynaptic_value = extract_value_customdict(mecotc,chemical_synapse[1])

        connector_connectivity_pre_idx = np.where((connectivity_type == presynaptic_value))[0]
        connector_connectivity_post_idx = np.where((connectivity_type == postsynaptic_value))[0]

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

        # build graph
        G = nx.DiGraph()
        G.add_nodes_from(np.unique(connectivity_skeletonid))
        for k,v in ds.items():
            for preskelid in v[const.PRESYNAPTIC]:
                for postkelid in v[const.POSTSYNAPTIC]:
                    if G.has_edge(preskelid, postkelid):
                        G.edge[preskelid][postkelid]['synapse'] += 1
                    else:
                        G.add_edge(preskelid, postkelid, weight=1)

        return G

    def get_skeleton_dict(self):
        """ Return dictionary keyed by skeleton id containing as value
        the skeletons as subgraph structure
        """
        # retrieve unique identifiers of skeletons
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
