from nose.tools import assert_true

from ...dataset.testcircuit import testcircuit
from ..network import NetworkAnalyzer


def test_network_networkconnectivity():
    """Test NetworkAnalyzer network_connectivity
    """
    nal = NetworkAnalyzer(testcircuit)

    assert_true(nal.network_connectivity.nodes() == [500, 100])
    edges = [(100, 500, {'weight': 1})]
    assert_true(nal.network_connectivity.edges(data=True) == edges)
