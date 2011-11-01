"""
Interfacing CATMAID (web UI, database, image tiles), SIPNet (Jan Funke), and NeuroHDF

Stage 1: From CATMAID to NeuroHDF

Select CATMAID
- project
  - id
- stack
  - id
  - dimension
  - scaling
- overlay id / new overlay
- ROI to process
  - z-index range
  - x coordinate range
  - y coordinate range

Stage 2: Call SIPNet. What is the API?
- Required parameters and image data location
- Output location/format

Stage 3: Export SIPNet output to CATMAID


Stage 4: Assignment correction between slices from CATMAID

"""
import h5py
import numpy as np
import json
import Image
from glob import glob
import os.path as op

projectid = 3
stackid = 3

datapath = '/home/stephan/data/cat-neuropil-reconstruction'
image_tiles_base = ''
fnamepattern = "*.tif"
nfile = 'test.hdf5'

resolution = (5,5,50)
files = sorted(glob(op.join(datapath, fnamepattern) ))
z_dim = len(files)

# discover size
imgarr = np.asarray(Image.open(files[0]))
dtype = imgarr.dtype
x_dim, y_dim = imgarr.shape
dimension = (x_dim, y_dim, z_dim)

nhdf = h5py.File( op.join(datapath, nfile), mode='a')

project_node = nhdf.create_group( str(projectid ))
stack_node = project_node.create_group( str(stackid) )

stack_node.attrs["dimension"] = dimension
stack_node.attrs["resolution"] = resolution

stack_data = stack_node.create_dataset('data', dimension, dtype=dtype, maxshape=dimension,compression='lzf', shuffle=True)

for i,fname in enumerate(files):
    print("Work on file %s".format(fname))
    f = Image.open(fname)
    stack_data[:,:,i] = np.asarray(f)
    del f

# add an overlay
overlay1 = stack_node.create_dataset('1', (10,10,5), dtype=np.uint8, compression='lzf', shuffle=True)
# translation in x,y,z directions. be sure to check the bounds
overlay1.attrs["translation"] = (50,50,10)
overlay1.attrs["sipnet_parameter_xxx"] = 1234
# interpretation of the labels: membrane, cell interior/exterior, synapse, mitochondria, etc.
# creation date

# *******
# Export memory-mapped datablock into tiff files
export_fnamepattern = 'myimage_%04d.tiff'
block = nhdf["3"]["3"]["data"]
z_dim = block.shape[2]

for i in xrange(z_dim):
    print("Work on z-Index {0}".format(i))
    fname = op.join(datapath,export_fnamepattern % (i+1) )
    # FIXME: is this efficiently fetched?
    im = Image.fromarray( block[:,:,i] )
    im.save( fname, 'TIFF' )
    del im

# *******
# Export skeletons from labeled block (to export to CATMAID)

# *******
# Merge all overlays into big overlay for export to CATMAID image pyramid
# Do intelligent boundary checking to minimally update slices

nhdf.close()
# nhdf = h5py.File( op.join(datapath, nfile), mode='a')
