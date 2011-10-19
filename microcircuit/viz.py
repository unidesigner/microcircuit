import networkx as nx
import types
import pylab

# wrap fos display of circuit

# wrap plot of connection matrix
# using metadata and coloring

# http://matplotlib.sourceforge.net/mpl_examples/pylab_examples/broken_barh.py

def show(connectome, skeleton_order, use_label, display_parameters):

    if connectome.graph is None:
        raise Exception("Connectome needs to have a valid graph")

    labels = []
    for ele in skeleton_order:
        labels.append( connectome.metadata[ele]['name'] )
    print "labels", labels

    fig = pylab.figure()
    ax = fig.add_subplot(111)

    ax.set_ylabel('Neurons')
    ax.set_yticks(range(len(labels)))
    labels.reverse()
    ax.set_yticklabels(labels)

    ax.set_xlabel('Neurons')
    ax.set_xticks(range(len(labels)))
    labels.reverse()
    ax.set_xticklabels(labels) # reverse back

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
                y.append(skeleton_order.index(v))
                if not scalelist is None:
                    scalelist.append(scale(data[relation]))
        y.reverse()
        print x,y,scalelist,scale,color,mark

        if scalelist is None and not scale is None: # TODO: correct?
            pylab.scatter(x, y, s=scale, c=color,marker=mark)
        else:
            pylab.scatter(x, y, s=scalelist, c=color,marker=mark)

    pylab.show()
