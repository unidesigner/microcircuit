import microcircuit.constants as const
from microcircuit.viz import show
from microcircuit.dataset.testcircuit001 import testcircuit as tc
from microcircuit.transforms.modularization import create_wiring_diagram

connectome = create_wiring_diagram(tc)
para = {
    const.CONNECTOME_CHEMICAL_SYNAPSE: {
        'marker': 'o',
        'c': 'r',
        's': 100
    },
    const.CONNECTOME_ELECTRICAL_SYNAPSE: {
        'marker': '^',
        'c': 'b',
        's': (lambda x:x*100.)
    }
}
nodes = connectome.graph.nodes()
print "nodes", nodes
print "sorted", sorted(connectome.graph.nodes())
#nodes = [111, 222, 333, 444, 555, 666]
nodes = sorted(nodes)
b=show(connectome, skeleton_order=nodes, use_label=True, display_parameters=para)
