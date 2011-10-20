import microcircuit.constants as const
from microcircuit.viz import show
import networkx as nx
from microcircuit.connectome import Connectome

a=nx.DiGraph()
a.add_edge(1,2, {const.CONNECTOME_CHEMICAL_SYNAPSE:1, const.CONNECTOME_ELECTRICAL_SYNAPSE:2})
a.add_edge(2,1, {const.CONNECTOME_ELECTRICAL_SYNAPSE:2})

me = {'name' : 'testcircuit00244',
            'neuronmap': {
                1: {'name':'A', 'type': 'Sensory neuron'},
                2: {'name':'B', 'type': 'Interneuron'}
            }}

connectome = Connectome(metadata=me['neuronmap'], graph=a)
para = {
    const.CONNECTOME_CHEMICAL_SYNAPSE: {
        'marker': 'o',
        'c': 'r',
        's': 100
    },
    const.CONNECTOME_ELECTRICAL_SYNAPSE: {
        'marker': '^',
        'c': 'b',
        's': (lambda x:x*10.)
    }
}
nodes = connectome.graph.nodes()
print "node", nodes
b=show(connectome, skeleton_order=nodes, use_label=True, display_parameters=para)
