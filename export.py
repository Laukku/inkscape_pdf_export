# Config script for inkscape_pdf_export
import sys, os
# Temporarily add directory where inkscape_pdf_export module is located to system path so it can be imported
sys.path.insert(0, r'C:\this\is\where\I\keep\my\module')
import inkscape_pdf_export


curdir = os.getcwd() # Location of this python script, which is assumed to be in the same folder as the SVG file
SVGfile = "MySVGfile.svg" # SVG file to be sliced into PDFs
# Run:
inkscape_pdf_export.export(curdir+"\\"+SVGfile, overwrite=True)
