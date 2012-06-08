import microcircuit as mc

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.units import inch
from glob import glob
import os



filename = '/home/stephan/abd15circuit.hdf'
hdf_path = '/Microcircuit'
inputdir = '/tmp/out'
outpdf = '/home/stephan/out.pdf'
width = 1898
height = 1103
ext = '*.png'


circuit=mc.load_neurohdf(filename, hdf_path)

files = sorted(glob(os.path.join(inputdir, ext)))
c = canvas.Canvas(outpdf)

# empty start page
c.setPageSize((width,height))
c.showPage()
c.save()


for pic in files:
    print pic
    skeleton_id = int(os.path.split(pic)[1].split('_')[0])
    info = ' | '.join( circuit.get_skeleton_allnames( skeleton_id ) )
    c.setPageSize((width,height))
    c.drawImage(pic, 0,0, width, height)
    c.setFont("Helvetica", 30)
    c.drawString( 10,10, info )
    c.showPage()
    c.save()
