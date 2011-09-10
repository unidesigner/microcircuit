
from .base import BaseAnalyzer


class SpatialAnalyzer(BaseAnalyzer):
    """Analyzer object for topological analysis"""

    def __init__(self, input=None, method=None):
        """
        Parameters
        ---------
        """
        BaseAnalyzer.__init__(self, input)
        self.graph = input.graph
