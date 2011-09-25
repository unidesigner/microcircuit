import os.path as op

from nose.tools import assert_true
from numpy.testing import assert_array_almost_equal

import numpy as np
from ..dataset import testcircuit
from ..circuit import Circuit


def test_circuit():
    """Create circuit
    """
    mytestcircuit = Circuit(
            vertices=testcircuit.vert, connectivity=testcircuit.conn,
            vertices_properties=testcircuit.vertices_properties,
            connectivity_properties=testcircuit.connectivity_properties,
            metadata=testcircuit.metadata
    )
    map_dict = {0: 10,
                1: 11,
                2: 200,
                3: 20,
                4: 21,
                5: 22}
    assert_true(mytestcircuit.map_vertices_idx2id == map_dict)


def test_circuitasgraph():
    """Test testcircuit as graph
    """
    circuitgraph = testcircuit.testcircuit.asgraph(add_attributes=True)

    assert_true(circuitgraph.number_of_nodes() == 6)
    assert_true(circuitgraph.number_of_edges() == 5)
    assert_true(circuitgraph.graph['name'] == 'testcircuit')
