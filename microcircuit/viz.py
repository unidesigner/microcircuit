import networkx as nx
from pylab import *

# wrap fos display of circuit

# wrap plot of connection matrix
# using metadata and coloring

# http://matplotlib.sourceforge.net/mpl_examples/pylab_examples/broken_barh.py

def show(connectome):

    if connectome.graph is None:
        raise Exception("Connectome needs to have a valid graph")

    m=nx.to_numpy_matrix(connectome.graph)
    imshow( m, vmin=m.min(), vmax=m.max(), interpolation='nearest')
    show()