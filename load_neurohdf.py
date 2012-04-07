# Load NeuroHDF exported from CATMAID

import microcircuit as mc
c=mc.load_neurohdf('test.hdf', '/Microcircuit')
sk = c.get_skeleton( 139117 )
print sk.get_total_length()
print sk.get_neuron_name()
print sk.get_incoming_connector_nodes()