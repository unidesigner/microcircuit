from glob import glob
import os

import microcircuit as mc

from reportlab.pdfgen import canvas
from reportlab.lib import colors


#################

filename = '/home/stephan/abd15circuit.hdf'
hdf_path = '/Microcircuit'
inputdir = '/tmp/out'
outpdf = '/home/stephan/abd1.5-md-da.pdf'
width = 1898
height = 1103
ext = '*.png'

title = 'Drosophila L1 VNC abdominal segment'
lab = 'Cardona lab'

pid = 4
translation = 0

url = 'http://localhost/catmaid-test/?pid={pid}&zp={zp}&yp={yp}&xp={xp}&tool=tracingtool&active_skeleton_id={active_skeleton_id}&active_node_id={node_id}&sid0={sid0}&s0={s0}'

###################

circuit = mc.load_neurohdf(filename, hdf_path)

files = sorted(glob(os.path.join(inputdir, ext)))
files.reverse()

c = canvas.Canvas(outpdf)
c.setTitle( title )
c.setPageSize((width,height))

c.setFont("Helvetica", 80)
c.drawString( 100, height/2., title )
c.setFont("Helvetica", 50)
c.drawString( 100, height/2.-150, lab )
c.showPage()
c.save()

for pic in files:
    print pic
    fname = os.path.split(pic)[1]
    nr_of_nodes, skeleton_id, rest = fname.split('_')
    nr_of_nodes = int(nr_of_nodes)
    skeleton_id = int(skeleton_id)
    info = ' | '.join( circuit.get_skeleton_allnames( skeleton_id ) )
    c.setPageSize((width,height))
    c.drawImage(pic, 0,0, width, height)
    c.setFont("Helvetica", 30)
    c.drawString( 10,10, info )
    c.drawString( 10,40, 'Skeleton: %s' % str(skeleton_id) )

    vert, ids = circuit.get_skeleton_vertices_and_ids( skeleton_id )
    xp,yp,zp = vert[0,:]
    node_id = ids[0]
    url_def = url.format(
        pid = pid,
        zp = int(zp)-translation,
        yp = int(yp),
        xp = int(xp),
        active_skeleton_id = skeleton_id,
        node_id = node_id,
        sid0 = 4,
        s0 = 0
    )
    r1 = (10,70,60,120)
    c.linkURL( url_def, r1, thickness=4, color=colors.green)

    c.showPage()
    c.save()
