import networkx as nx
import types
try:
    import pylab
except:
    pass
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
        labels = copy(skeleton_order) # otherwise subsequent manipulation of label would impact order
    print "labels", labels

    nr_labels = len(labels)

    fig = pylab.figure()

    ax = fig.add_subplot(111)
    ax.autoscale_view(scalex=False,scaley=False)
    
    ax.set_ylabel('Neurons')
    labelsy = copy(labels)
    labelsy.reverse()
    ax.set_yticks(range(nr_labels))
    ax.set_yticklabels(labelsy)

    ax.set_xlabel('Neurons')
    ax.set_xticks(range(nr_labels))
    labelsx = copy(labels)
    #print "labelsx", labelsx
    #labelsx.reverse()
    #print "labelsx reversed", labelsx
    ax.set_xticklabels(labelsx) # reverse back

    ax.xaxis.set_label_position("top")
    ax.xaxis.set_ticks_position("top")

    #print "skeleton order", skeleton_order
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
                x.append( len(skeleton_order)-1-skeleton_order.index(u) )
                #print "found u at index i, to new", u, skeleton_order.index(u), len(skeleton_order)-1-skeleton_order.index(u)
                y.append( skeleton_order.index(v) )
                #print "found v at index i, to new", v, skeleton_order.index(v), skeleton_order.index(v)
                if not scalelist is None:
                    scalelist.append(scale(data[relation]))
        
        #print x,y,scalelist,scale,color,mark
        # TODO: problem with visibility depending on the order?
        if scalelist is None and not scale is None: # TODO: correct?
            pylab.scatter(x, y, s=scale, c=color,marker=mark)
        else:
            pylab.scatter(x, y, s=scalelist, c=color,marker=mark)

    ax.set_ybound(-0.5, len(labels)-0.5)
    ax.set_xbound(-0.5, len(labels)-0.5)
    pylab.show()

    return fig
