import numpy as np
import networkx as nx
from IPython.utils import autoattr as desc
import microcircuitry.algorithms.metrics.skeleton as skeletonmetrics

from .base import BaseAnalyzer


class MeasureAnalyzer(BaseAnalyzer):
    """Analyzer object for measures for skeletons"""

    def __init__(self, circuit=None, method=None):
        """ Compute similarities between skeletons modularized
        with `id` of connectivity_properties

        Parameters
        ----------

        method : str
            'nr_vertices'
        """
        BaseAnalyzer.__init__(self, input)
        if method is None:
            self.method = {'this_method': 'nr_vertices'}
        else:
            self.method = method
        self.graph = circuit.asgraph(add_attributes=True)
        # retrieve unique identifiers of skeletons
        if "id" in circuit.connectivity_properties:
            idarr = circuit.connectivity_properties["id"]["data"]
            uniqueidarr = np.unique(idarr)
            self.id_idx = dict.fromkeys(uniqueidarr)
            for id in uniqueidarr:
                # compute list of indices for each identifier
                idx = np.where(idarr == id)[0]
                # TODO: does it include attributes?
                self.id_idx[id] = self.graph.subgraph(idx)
        if "type" in circuit.connectivity_properties:
            self.type = circuit.connectivity_properties["type"]
        else:
            self.type = None

    @desc.auto_attr
    def measure(self):
        ret = dict.fromkeys(self.id_idx.keys())
        for id, value in self.id_idx.items():
            if self.method['this_method'] == 'nr_vertices':
                ret[id] = value.number_of_nodes()
            elif self.method['this_method'] == 'nr_connectivity':
                ret[id] = value.number_of_edges()
            elif self.method['this_method'] == 'total_path_length':
                ret[id] = skeletonmetrics.sum_edge_value(value,
                                                         edge_key='length')
            elif self.method['this_method'] == 'compartmental_path_length':
                if self.type is None:
                    raise Exception("Require `type` connectivity_property" +
                                    "for this method")
                ret[id] = skeletonmetrics.compartmental_path_length(value,
                                self.type["metadata"]["value"])
            # TODO: more! http://farsight-toolkit.org/wiki/L_Measure_functions
        return ret
