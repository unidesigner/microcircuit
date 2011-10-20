import microcircuit.constants as const
from microcircuit.viz import show
from microcircuit.dataset.testconnectome001 import testconnectome

para = {
    const.CONNECTOME_CHEMICAL_SYNAPSE: {
        'marker': 'o',
        'c': 'r',
        's': 50
    },
    const.CONNECTOME_ELECTRICAL_SYNAPSE: {
        'marker': '^',
        'c': 'b',
        's': 40
    }
}
nodes = testconnectome.graph.nodes()
b=show(testconnectome, skeleton_order=nodes, use_label=True, display_parameters=para)
