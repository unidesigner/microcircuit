from fos import *
import numpy as np
import sys
import h5py
import microcircuit as mc
import os

filename = '/home/stephan/abd15circuit.hdf'
hdf_path = '/Microcircuit'
temp_image_dir = '/tmp/out'

name_whitelist = ['md (11)', 'md (10)']
#name_whitelist = ['Lineages', 'LEFT', 'RIGHT']

outline_id = 17612674
long_id = 17612866
width = 1898
height = 1103

#############

c=mc.load_neurohdf(filename, hdf_path)
all_skeletons = c.get_all_skeletons()

conn_color_map = {
    1 : np.array([[0.0, 0.0, 0.0, 1.0]]),
    2 : np.array([[1.0, 0.0, 0.0, 1.0]]),
    3 : np.array([[0.0, 0.0, 1.0, 1.0]])
}

def create_microcircuit(skeleton_id, vertices_location, connectivity_skeleton_with_synapse, connectivity_skeletonid, miin, connectivity_type):
    act = Microcircuit(
        name=str(skeleton_id),
        vertices_location=vertices_location,
        connectivity=connectivity_skeleton_with_synapse,
        connectivity_ids=connectivity_skeletonid-miin,
        connectivity_label=connectivity_type,
        connectivity_label_metadata=[
                { "name" : "skeleton", "value" : "1" },
                { "name" : "presynaptic", "value" : "2" },
                { "name" : "postsynaptic", "value" : "3" }
        ],
        connectivity_colormap=conn_color_map,
        skeleton_linewidth=2.5,
        connector_size=2.0,
        global_deselect_alpha=0.1
    )
    return act


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

# Fos window
white = (1.0,1.0,1.0)
black = (0.0,0.0,0.0)
w = Window( width = width, height = height, bgcolor = white, dynamic = True )

mytransform = Transform3D(np.eye(4))
mytransform.set_scale(-1, -1, 1)
mytransform.set_translation( 0, 0, 0 )
region = Region(
    regionname = "Main",
    transform = mytransform,
    aabb_color = (1.0, 1.0, 1.0, 1.0),
    activate_aabb = False
)
w.add_region ( region )
# w.hide()

outline_actor=create_microcircuit( *c.get_fos_microcircuit( outline_id, scale_factor = 100. ))
long_actor=create_microcircuit( *c.get_fos_microcircuit( long_id, scale_factor = 100. ))

def process_skeleton( allnames ):
    for ele in name_whitelist:
        if bool(len([i for i in allnames if ele in i])):
            return True
    return False

def display():
    for skeleton_id in all_skeletons:

        allnames = c.get_skeleton_allnames( skeleton_id )
        nr_of_nodes = c.get_skeleton_number_of_nodes( skeleton_id )
        print 'Skeleton', skeleton_id, nr_of_nodes
        if not process_skeleton( allnames ):
            #print 'Skipped'
            continue

        filename = allnames[-1]
        region.add_actor(outline_actor,trigger_update=True)

        r=create_microcircuit( *c.get_fos_microcircuit( skeleton_id, scale_factor = 100. ) )
        region.add_actor(r,trigger_update=False)

        # XY view
        w.refocus_camera()
        # update zoom
        w.glWidget.ortho_zoom(0.25)
        #w.screenshot( '/tmp/out/%s_XY_(skeleton %i).png' % (filename, skeleton_id) )
        w.screenshot( os.path.join(temp_image_dir, '%i_xy.png' % skeleton_id ) )

        # remove outline actor
        region.remove_actor( outline_actor )

        # XZ View
        region.add_actor(long_actor,trigger_update=True)
        w.refocus_camera()
        w.glWidget.world.camera.rotate_around_focal( -1.5, 'right' )
        w.glWidget.ortho_zoom(0.15)
        #w.screenshot( '/tmp/out/%s_XZ_(skeleton %i).png' % (filename, skeleton_id) )
        w.screenshot( os.path.join(temp_image_dir, '%i_xz.png' % skeleton_id ) )

        region.remove_actor( long_actor )
        region.remove_actor( r )
