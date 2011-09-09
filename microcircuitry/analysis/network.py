import numpy as np
import networkx as nx
from IPython.utils import autoattr as desc

from .base import BaseAnalyzer


class NetworkAnalyzer(BaseAnalyzer):
    """Analyzer object for network/graph analysis"""

    def __init__(self, input=None):
        """
        Parameters
        ---------
        """
        BaseAnalyzer.__init__(self, input)

        self.graph = input.asgraph()

    @desc.auto_attr
    def centrality(self):
        return nx.algorithms.centrality.betweenness_centrality(self.graph)
