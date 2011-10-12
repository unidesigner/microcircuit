import numpy as np
import networkx as nx
from IPython.utils import autoattr as desc

from .base import BaseAnalyzer
import microcircuit.constants as const
from microcircuit.utils import extract_value_customdict


class NetworkAnalyzer(BaseAnalyzer):
    """Analyzer object for network/graph analysis"""

    def __init__(self, input=None):
        """
        Parameters
        ---------
        """
        BaseAnalyzer.__init__(self, input)

        self.circuit = input
        self.graph = input.asgraph()

    @desc.auto_attr
    def network_connectivity(self):
        """Extract a network from the input circuit where
        nodes are skeletons and edges are the number of synaptic
        connections
        """
        metc = self.circuit.get_vertices_property(const.TYPE, True)
        mecotc = self.circuit.get_connectivity_property(const.TYPE, True)

        connector_value = extract_value_customdict(metc,
                                                   const.CONNECTOR_NODE)
        presynaptic_value = extract_value_customdict(mecotc,
                                                     const.PRESYNAPTIC_TO)
        postsynaptic_value = extract_value_customdict(mecotc,
                                                      const.POSTSYNAPTIC_TO)

        vertices_type = self.circuit.get_vertices_property(const.TYPE)
        connectivity_type = self.circuit.get_connectivity_property(const.TYPE)
        connectivity_skeletonid = self.circuit.get_connectivity_property(
            const.SKELETON_ID)
        connector_idx = set(np.where(vertices_type == connector_value)[0])

        # loop over connectivity and extract connectors
        # need to build potentially all polyadic (MxN) connectors
        # key: vertices connector index, value: skeleton id
        pre = dict.fromkeys(connector_idx, [])
        post = dict.fromkeys(connector_idx, [])

        for i, uv in enumerate(self.circuit.connectivity):
            u, v = uv
            if v in connector_idx:
                # check if pre or post
                if connectivity_type[i] == presynaptic_value:
                    pre[v].append(connectivity_skeletonid[i])
                elif connectivity_type[i] == postsynaptic_value:
                    post[v].append(connectivity_skeletonid[i])
                else:
                    print("Target node {0} neither pre nor postsynaptic".
                          format(v))

        G = nx.DiGraph()
        G.add_nodes_from(np.unique(connectivity_skeletonid))
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
                print('Connector with either zero pre or post connectivity')

        return G

    @desc.auto_attr
    def centrality(self):
        return nx.algorithms.centrality.betweenness_centrality(self.graph)
