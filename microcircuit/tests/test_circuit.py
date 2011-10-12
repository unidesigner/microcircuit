import os.path as op

from nose.tools import assert_true
from numpy.testing import assert_array_almost_equal

import numpy as np
from ..dataset import testcircuit001, testcircuit002
from ..circuit import Circuit

def test_circuit_001():
    """Create testcircuit 001
    """
    mytestcircuit001 = Circuit(
            vertices=testcircuit001.vert, connectivity=testcircuit001.conn,
            vertices_properties=testcircuit001.vertices_properties,
            connectivity_properties=testcircuit001.connectivity_properties,
            metadata=testcircuit001.metadata
    )
    map_dict = {0:10,
                1:11,
                2:200,
                3:20,
                4:21,
                5:22}
    assert_true(mytestcircuit001.map_vertices_idx2id==map_dict)

def test_circuitasgraph_001():
    """Test testcircuit001 as graph
    """
    circuitgraph = testcircuit001.testcircuit.asgraph(add_attributes=True)

    assert_true(circuitgraph.number_of_nodes()==6)
    assert_true(circuitgraph.number_of_edges()==5)
    assert_true(circuitgraph.graph['name']=='testcircuit001')


def test_circuit_002():
    """Create testcircuit 002
    """
    mytestcircuit002 = Circuit(
            vertices=testcircuit002.vert, connectivity=testcircuit002.conn,
            vertices_properties=testcircuit002.vertices_properties,
            connectivity_properties=testcircuit002.connectivity_properties,
            metadata=testcircuit002.metadata
    )
    map_dict = {0: 100,
         1: 101,
         2: 102,
         3: 103,
         4: 104,
         5: 105,
         6: 106,
         7: 107,
         8: 108,
         9: 109,
         10: 110,
         11: 111,
         12: 112,
         13: 113,
         14: 114,
         15: 115,
         16: 116,
         17: 117,
         18: 118}

    assert_true(mytestcircuit002.map_vertices_idx2id==map_dict)

def test_circuitasgraph_002():
    """Test testcircuit002 as graph
    """
    circuitgraph = testcircuit002.testcircuit.asgraph(add_attributes=True)

    assert_true(circuitgraph.number_of_nodes()==19)
    assert_true(circuitgraph.number_of_edges()==20)
    assert_true(circuitgraph.graph['name']=='testcircuit002')
