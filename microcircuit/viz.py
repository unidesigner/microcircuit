import networkx as nx
import types
import pylab
from copy import copy

# wrap fos display of circuit

# wrap plot of connection matrix
# using metadata and coloring

# http://matplotlib.sourceforge.net/mpl_examples/pylab_examples/broken_barh.py

def show(connectome, skeleton_order, use_label, display_parameters):

    if connectome.graph is None:
        raise Exception("Connectome needs to have a valid graph")

    labels = []

    if use_label and not connectome.metadata is None:
        for ele in skeleton_order:
            if connectome.metadata.has_key(ele):
                labels.append( connectome.metadata[ele]['name'] )
    else:
        labels = skeleton_order
    print "labels", labels

    nr_labels = len(labels)

    fig = pylab.figure()

    ax = fig.add_subplot(111)
    ax.autoscale_view(scalex=False,scaley=False)
    
    ax.set_ylabel('Neurons')
    labels.reverse()
    ax.set_yticks(range(nr_labels))
    ax.set_yticklabels(labels)

    ax.set_xlabel('Neurons')
    ax.set_xticks(range(nr_labels))
    labelsx = copy(labels)
    labelsx.reverse()
    ax.set_xticklabels(labelsx) # reverse back

    ax.xaxis.set_label_position("top")
    ax.xaxis.set_ticks_position("top")

    for relation, para in display_parameters.items():

        # scaling for each
        if para.has_key('s'):
            scale = para['s']
        else:
            scale = None
        # color
        if para.has_key('c'):
            color = para['c']
        else:
            color = None
        # marker
        if para.has_key('marker'):
            mark = para['marker']
        else:
            mark = None
        x=[]; y=[]
        if isinstance(scale,types.FunctionType):
            scalelist = []
        else:
            scalelist = None
        for u,v,data in connectome.graph.edges_iter(data=True):
            if not (u in skeleton_order and v in skeleton_order):
                continue
            if data.has_key(relation):
                x.append(skeleton_order.index(u))
                y.append(nr_labels-skeleton_order.index(v))
                if not scalelist is None:
                    scalelist.append(scale(data[relation]))
        y.reverse()
        print x,y,scalelist,scale,color,mark

        if scalelist is None and not scale is None: # TODO: correct?
            pylab.scatter(x, y, s=scale, c=color,marker=mark)
        else:
            pylab.scatter(x, y, s=scalelist, c=color,marker=mark)

    ax.set_ybound(-0.5, len(labels)-0.5)
    ax.set_xbound(-0.5, len(labels)-0.5)
    pylab.show()

    return fig
