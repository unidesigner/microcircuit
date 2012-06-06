from fos import *
import numpy as np
import sys
import h5py
import microcircuit as mc

filename = '/home/stephan/stem1circuit.hdf'

c=mc.load_neurohdf(filename, '/Microcircuit')
all_skeletons = c.get_all_skeletons()

# select interesting skeletons

outline_id = 17595541

#####################3

f=h5py.File( filename, 'r')

vertices_id = f['Microcircuit']['vertices']['id'].value
vertices_location = f['Microcircuit']['vertices']['location'].value
connectivity_id = f['Microcircuit']['connectivity']['id'].value
connectivity_skeletonid = f['Microcircuit']['connectivity']['skeletonid'].value
connectivity_type = f['Microcircuit']['connectivity']['type'].value

vertices_location = ((vertices_location - np.mean(vertices_location, axis=0))).astype(np.float32) / 100.

def map_vertices_id2index(vertices_id):
    map_vertices_id2index = dict(zip(vertices_id,range(len(vertices_id))))
    connectivity_indices = np.zeros( connectivity_id.shape, dtype=np.uint32 )
    for i,c in enumerate(connectivity_id):
        connectivity_indices[i,0]=map_vertices_id2index[connectivity_id[i,0]]
        connectivity_indices[i,1]=map_vertices_id2index[connectivity_id[i,1]]
    return connectivity_indices

conn_color_map = {
    #1 : np.array([[1.0, 1.0, 0.0, 1.0]]),
    1 : np.array([[0.0, 0.0, 0.0, 1.0]]),
    2 : np.array([[1.0, 0.0, 0.0, 1.0]]),
    3 : np.array([[0.0, 0.0, 1.0, 1.0]])
}

miin=connectivity_skeletonid.min()-1
connectivity_skeletonid = connectivity_skeletonid-miin

w = Window( width = 1200, height = 800, bgcolor = (1.0,1.0,1.0), dynamic = True )

mytransform = Transform3D(np.eye(4))
mytransform.set_scale(-1, -1, 1)

region = Region( regionname = "Main", transform = mytransform, aabb_color=(0.0, 0.0, 0.0, 1.0))

act = Microcircuit(
    name="Testcircuit",
    vertices_location=vertices_location,
    connectivity=map_vertices_id2index(vertices_id),
    connectivity_ids=connectivity_skeletonid,
    connectivity_label=connectivity_type,
    connectivity_label_metadata=[
            { "name" : "skeleton", "value" : "1" },
            { "name" : "presynaptic", "value" : "2" },
            { "name" : "postsynaptic", "value" : "3" }
    ],
    connectivity_colormap=conn_color_map,
    skeleton_linewidth=2.5,
    connector_size=2.0,
    global_deselect_alpha=0.0
)

region.add_actor( act )
region.add_actor( Axes( name = "3 axes", linewidth = 5.0) )

#values = np.ones( (len(vertices_location)) ) * 0.1
#region.add_actor( Scatter( "MySphere", vertices_location[:,0], vertices_location[:,1], vertices_location[:,2], values, iterations = 2 ) )

w.add_region ( region )

act.deselect_all()

# act.select_skeleton( [17611396-miin] )

w.refocus_camera()
w.hide()

###############33
import time
#interesting = [139838+miin]
interesting = all_skeletons[:200]

# XY
#Location: [  52.45831299  -14.4712677  -621.9798584 ]
#Focal point: [ 52.45831299 -14.4712677   -6.67984009]
#Look at direction : [ 0.  0.  1.]
#Y up direction : [ 0.  1.  0.]
#Right direction : [-1.  0.  0.]

def screen():
    for skeleton_id in interesting:
        print 'skeletonid', skeleton_id
        sk = c.get_skeleton( skeleton_id )
        # name = '_'.join( sk.allnames )
        name = sk.allnames[-1]
        print sk.number_of_nodes()
        if sk.number_of_nodes() < 10:
            continue
        act.deselect_all()

        act.select_skeleton( [outline_id-miin] )

        act.select_skeleton( [skeleton_id-miin] )
        # w.refocus_camera()
        w.glWidget.world.camera.location = np.array([  52.45831299,  -14.4712677 , -621.9798584 ], dtype=np.float32)
        w.glWidget.world.camera.focal = np.array([ 52.45831299, -14.4712677 ,  -6.67984009], dtype=np.float32)
        w.glWidget.world.camera.yuppoint = np.array([  52.45831299,  -13.4712677 , -621.9798584 ], dtype=np.float32)
        w.glWidget.updateGL()
        w.screenshot( '/tmp/skeleton_%i_xy_%s.png' % (skeleton_id,name) )

        w.glWidget.world.camera.location = np.array([  48.88044739,  630.77679443,  -14.08395767], dtype=np.float32)
        w.glWidget.world.camera.focal = np.array([ 52.45831299, -14.4712677 ,  -6.67984009], dtype=np.float32)
        w.glWidget.world.camera.yuppoint = np.array([  48.87618256,  630.78814697,  -13.08396912], dtype=np.float32)
        w.glWidget.updateGL()
        w.screenshot( '/tmp/skeleton_%i_xz_%s.png' % (skeleton_id,name) )