import networkx as nx
import numpy as np

from microcircuit.utils import extract_value_customdict
import constants as const

class Connectome(object):

    def __init__(self, metadata=None, circuit=None):
        """Connectome or Wiring Diagram. Represents a graph view on a `Circuit`
        """

        # includes neuronmap that maps neuron/skeletonid to label etc.
        self.metadata = metadata

        # the base Circuit that used to construct this connectome
        self.circuit = circuit

        if not circuit is None:
            # dictionary of skeleton objects keyed by their id
            self.skeletons = self.skeleton_dict()

            # NetworkX graph with nodes (skeletons) and edges (connectivity)
            self.graph = self.network_connectivity()
        else:
            self.skeletons = None
            self.graph = None

    def network_connectivity(self):
        """Extract a network from the input circuit where
        nodes are skeletons and edges are the number of synaptic
        connections
        """
        metc = self.circuit.get_vertices_property(const.TYPE, True)[1]
        mecotc = self.circuit.get_connectivity_property(const.TYPE, True)[1]

        vertices_type = self.circuit.get_vertices_property(const.TYPE)
        connectivity_type = self.circuit.get_connectivity_property(const.TYPE)
        connectivity_skeletonid = self.circuit.get_connectivity_property(const.SKELETON_ID)

        connector_value = extract_value_customdict(metc,
                                                   const.CONNECTOR_NODE)

        # define valid transform of M:N connector pairs and whether directional
        # not directional implies bidirectional
        chemical_synapse = (const.PRESYNAPTIC, const.POSTSYNAPTIC, True)
        gap_junctions = (const.GAP_JUNCTION, const.GAP_JUNCTION, False)

        presynaptic_value = extract_value_customdict(mecotc,chemical_synapse[0])
        postsynaptic_value = extract_value_customdict(mecotc,chemical_synapse[1])

        connector_idx = set(np.where(vertices_type == connector_value)[0])

        # loop over connectivity and extract connectors
        # need to build potentially all polyadic (MxN) connectors
        # key: vertices connector index, value: skeleton id
        pre = dict.fromkeys(connector_idx, [])
        post = dict.fromkeys(connector_idx, [])

        for i, uv in enumerate(self.circuit.connectivity):
            u, v = uv
            print "u,v", u,v
            if v in connector_idx:
                print "found presynaptic"
                # either presynaptic or gapjunction
                # check if pre or post
                if connectivity_type[i] == presynaptic_value:
                    # retrieve associated skeleton identifier
                    pre[v].append(connectivity_skeletonid[i])
                else:
                    print("Gap junction found!")

            elif u in connector_idx:
                print "found postsynaptic"
                # either postsynaptic or gapjunction
                if connectivity_type[i] == postsynaptic_value:
                    # retrieve associated skeleton identifier
                    post[u].append(connectivity_skeletonid[i])
                else:
                    print("Gap junction found")

        G = nx.DiGraph()
        G.add_nodes_from(np.unique(connectivity_skeletonid))
        # loop of connectors and add
        for cid in connector_idx:
            if not len(pre[cid]) == 0 and not len(post[cid]) == 0:
                # add M times N connectivity to network
                for u in pre[cid]:
                    for v in post[cid]:
                        # retrieve skeleton id for connectivity
                        if G.has_edge(u, v):
                            G.edge[u][v]['weight'] += 1
                        else:
                            G.add_edge(u, v, weight=1)
            else:
                print('Connector with either zero pre or post connectivity: {0}'.format(cid))

        return G

    def skeleton_dict(self):
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

    @staticmethod
    def fromcircuit(self, circuit):
        """ Extract Connectome from Circuit using skeleton identifiers
        to segregate the circuit

        """

        self.circuit = circuit

        self.graph = self.circuit.asgraph(add_attributes=True)

        self.graph = nx.DiGraph()
        # add nodes from skeleton identifiers
        self.graph.add_nodes_from( self.skeletons.keys() )

        # loop over skeletons
        for skeletonid, skeleton in self.skeletons.items():
            # we require some semantics of the connections
            # to correctly derive the high-level connectivity
            # e.g. chemical synapses vs. gap junctions or other associations
            # or also interpretation on the intrinsic connectivity of
            # a skeleton (not every skeleton is bipolar for instance)
            # it should be general enough
            pass
            
        # extract all presynaptic connections
            # loop over postsynaptic connections
            # get skeleton id
            # add relevant information to connectome (multi)
            # e.g. also number of vertices in the postsynaptic skeleton (e.g.
            # for partial or incomplete reconstructions)