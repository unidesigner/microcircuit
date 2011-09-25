import numpy as np
from IPython.utils import autoattr as desc
import microcircuit.algorithms.metrics.skeleton as skeletonmetrics

from .base import BaseAnalyzer
from ..transforms.modularization import unique_values

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
        uniqueidarr = unique_values(circuit, 'id', 'connectivity')
        if not uniqueidarr is None:
            # for each skeleton, use id as dictionary key
            self.skeleton_graphs = dict.fromkeys(uniqueidarr)
            # for each skeleton id, retrieve connectivity indices
            idarr = circuit.connectivity_properties["id"]["data"]
            for id in uniqueidarr:
                # compute list of indices for each identifier
                idx = np.where(idarr == id)[0]
                # TODO: does it include attributes?
                # store each skeleton as subgraph
                self.skeleton_graphs[id] = self.graph.subgraph(idx)
        if "type" in circuit.connectivity_properties:
            self.type = circuit.connectivity_properties["type"]
        else:
            self.type = None

    @desc.auto_attr
    def measure(self):
        ret = dict.fromkeys(self.skeleton_graphs.keys())
        for id, value in self.skeleton_graphs.items():
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
