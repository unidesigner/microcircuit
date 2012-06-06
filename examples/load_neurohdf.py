# Load NeuroHDF exported from CATMAID

import microcircuit as mc
import fos

c=mc.load_neurohdf('/home/stephan/stem1circuit.hdf', '/Microcircuit')

all_skeletons = c.get_all_skeletons()

sk = c.get_skeleton( all_skeletons[0] )
print sk.get_total_length()
print sk.get_neuron_name()
print sk.get_incoming_connector_nodes()