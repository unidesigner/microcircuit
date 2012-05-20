import numpy as np
import h5py

import constants as const

def load_neurohdf(filename, hdf5path, memmapped=False):
    """ Loads the circuit from a NeuroHDF file as exported from CATMAID

    Parameters
    ----------
    filename : str
        Path to the NeuroHDF file
    hdfpath : str
        HDF5 path to the irregular dataset containing the circuit
        e.g. /Microcircuit
    """
    if memmapped:
        raise NotImplementedError('Memmapped HDF5 reading not yet implemented')

    circuit = Circuit()

    f = h5py.File(filename, 'r')
    circuitdata_group=f[hdf5path]
    vertices_group = circuitdata_group.get('vertices')
    connectivity_group = circuitdata_group.get('connectivity')
    metadata_group = circuitdata_group.get('metadata')

    def helpdict(v):
        helpdict = dict.fromkeys( v.attrs.keys() )
        for k in helpdict:
            helpdict[k] = v.attrs.get(k)
        return helpdict

    for k,v in vertices_group.items():
        if k == 'id':
            circuit.vertices = vertices_group[k].value
        else:
            circuit.vertices_properties[k] = dict.fromkeys( [const.DATA, const.METADATA] )
            circuit.vertices_properties[k][const.DATA] = v.value
            circuit.vertices_properties[k][const.METADATA] = helpdict(v)
        print('Added vertices {0}'.format(k))

    for k,v in connectivity_group.items():
        if k == 'id':
            circuit.connectivity = connectivity_group[k].value
        else:
            circuit.connectivity_properties[k] = dict.fromkeys( [const.DATA, const.METADATA] )
            circuit.connectivity_properties[k][const.DATA] = v.value
            circuit.connectivity_properties[k][const.METADATA] = helpdict(v)

        print('Added connectivity {0}'.format(k))
    if metadata_group:
        for k,v in metadata_group.items():
            circuit.metadata[k] = dict.fromkeys( [const.DATA, const.METADATA] )
            circuit.metadata[k][const.DATA] = v.value
            circuit.metadata[k][const.METADATA] = helpdict(v)
        print('Added metadata {0}'.format(k))
    circuit._remap_vertices_id2indices()
    f.close()

    return circuit
