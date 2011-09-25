import networkx as nx
from IPython.utils import autoattr as desc

from .base import BaseAnalyzer
from ..transforms.modularization import unique_values

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

    def network_connectivity(self):
        """Extract a network from the input circuit where
        nodes are skeletons and edges is the number of synaptic
        connections
        """
        # retrieve the set of all skeleton ids to be used as node ids
        uniqueval = unique_values(self.circuit, 'id', 'connectivity')

        # retrieve all indices of connectors
        connector_idx = np.where(self.circuit.vertices_properties['label']['data'] == 2)
        
        # loop through connectivity, checking for each pre/post connection
        for u,v in self.circuit.connectivity:
            if v in connector_idx:
                # found a connector
                pass
                
        

    @desc.auto_attr
    def centrality(self):
        return nx.algorithms.centrality.betweenness_centrality(self.graph)
