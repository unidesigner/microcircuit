""" Retrieve C.elegans connectivity from Web and parse appropriately
"""

# see data/
# http://mit.edu/lrv/www/elegans/

from scipy.io import matlab
import os.path as op
import networkx as nx
import microcircuit.constants as const
from microcircuit.connectome import Connectome

mat = matlab.loadmat(op.join(op.dirname(op.abspath(__file__)), 'data', 'ConnOrdered_040903.mat'))

['A_init_t_ordered',
 '__header__',
 '__globals__',
 'Q_sorted',
 'Neuron_ordered',
 'Ag_t_ordered',
 '__version__']

metadata = {'name': 'testconnectome001',
            'neuronmap': {}}
for i,label in enumerate(mat['Neuron_ordered']):
    metadata['neuronmap'][i+1] = {'name': label[0][0]}

gap = mat['Ag_t_ordered']
gap[94,94]=0.0
gap[106,106]=0.0
gap[216,216]=0.0

graphgap = nx.from_numpy_matrix(gap.todense(), create_using=nx.DiGraph())
graphgap = nx.relabel_nodes(graphgap, (lambda x:x+1))
for u,v,d in graphgap.edges_iter(data=True):
    d[const.CONNECTOME_ELECTRICAL_SYNAPSE] = d['weight']
    del d['weight']

chem=mat['A_init_t_ordered']
graphchem = nx.from_numpy_matrix(gap.todense(), create_using=nx.DiGraph())
graphchem = nx.relabel_nodes(graphchem, (lambda x:x+1))
for u,v,d in graphchem.edges_iter(data=True):
    d[const.CONNECTOME_CHEMICAL_SYNAPSE] = d['weight']
    del d['weight']

# TODO: problem with merge
for u,v,d in graphchem.edges_iter(data=True):
    # TODO: how does it go over digraphs?
    # In addtion
    graphgap.add_edge(u,v, {const.CONNECTOME_CHEMICAL_SYNAPSE:d[const.CONNECTOME_CHEMICAL_SYNAPSE]})

testconnectome = Connectome(metadata=metadata['neuronmap'], graph=graphgap)