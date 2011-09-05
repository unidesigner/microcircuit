import numpy as np
import networkx as nx
from IPython.utils import autoattr as desc

from .base import BaseAnalyzer

class SpatialAnalyzer(BaseAnalyzer):
    """Analyzer object for spatial analysis"""

    def __init__(self, input=None, method=None):
        """
        Parameters
        ---------
        """
        BaseAnalyzer.__init__(self, input)

        self.graph = input.graph
        self.space_unit = input.space_unit

    @desc.auto_attr
    def total_path_length(self):
        # TODO: add space units, may overcomplicate it
        pass