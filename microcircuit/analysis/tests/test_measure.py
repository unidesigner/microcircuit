from nose.tools import assert_true

from ...dataset.testcircuit import testcircuit
from ..measure import MeasureAnalyzer


def test_measure_nr_vertices():
    """Test MeasureAnalyzer nr_vertices
    """
    manal = MeasureAnalyzer(testcircuit,
                            method={'this_method':
                                    'nr_vertices'})

    res_dict = {100: 2, 500: 3}

    assert_true(manal.measure == res_dict)


def test_measure_nr_connectivity():
    """Test MeasureAnalyzer nr_connectivity
    """
    manal = MeasureAnalyzer(testcircuit,
                            method={'this_method':
                                    'nr_connectivity'})

    print(manal.measure)

    res_dict = {100: 1, 500: 2}

    assert_true(manal.measure == res_dict)


def test_measure_total_path_length():
    """Test MeasureAnalyzer total_path_length
    """
    manal = MeasureAnalyzer(testcircuit,
                            method={'this_method':
                                    'total_path_length'})

    res_dict = {100: 7.071067810058594, 500: 11.216116428375244}

    assert_true(manal.measure == res_dict)


def test_measure_compartmental_path_length():
    """Test MeasureAnalyzer compartmental_path_length
    """
    manal = MeasureAnalyzer(testcircuit,
                            method={'this_method':
                                    'compartmental_path_length'})

    res_dict = {100: {1: 7.071067810058594, 2: 0.0, 3: 0.0, 4: 0.0},
        500: {1: 0.0, 2: 0.0, 3: 5.385164737701416, 4: 5.830951690673828}}

    assert_true(manal.measure == res_dict)
