# auto PDF export python script
# Mark pages with rectangles in SVG file. Only portrait view is supported.
# the script finds them and exports each area as a pdf
# margin - the rectangles can be smaller than a full page - centers on page

# To be used as a module. Include this file in a config script for each folder. For repeatability!


#################################################
import svgpathtools # For getting actual bounding box of SVG elements
# import xml.etree.ElementTree as ET
from lxml import etree # for finding nodes in SVG file
import ntpath # for operating on system paths
import os # Create directories
from shutil import copyfile # Copy files
import subprocess # for running inkscape from this script

def export(SVGfile, overwrite=True):
    # ns = {'svg': 'http://www.w3.org/2000/svg'}
    ns = {'dc':'http://purl.org/dc/elements/1.1/',
       'cc':'http://creativecommons.org/ns#',
       'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
       'svg':'http://www.w3.org/2000/svg',
       'default':'http://www.w3.org/2000/svg',
       'xlink':'http://www.w3.org/1999/xlink',
       'sodipodi':'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
       'inkscape':'http://www.inkscape.org/namespaces/inkscape'}
    # TODO: Replace with command line options
    curdir = os.getcwd() # Location of this python script / or the one calling this module
    # transformscale = -3.77953 # For some reason transforms are given in px (?) even if document units are set to equal mm # Only if you try to apply a transform to the root SVG node in inkscape
    # overwrite = False # Overwrite Inkscape export output pdf files
    targetdir = r"test_output"
    tempfile = targetdir+r"\tempfile.svg"
    os.makedirs(targetdir, exist_ok=True)
    # Change this if your PdfMerge is located somewhere else:
    pdfmergepath = r"C:\Program Files (x86)\PdfMerge\PdfMerge.exe"
    copyfile(SVGfile,tempfile)
    planname = ntpath.basename(SVGfile).split('.')[0]
    doctitle = planname.capitalize().replace("_", " ")
    print(doctitle)
    tree = etree.parse(SVGfile)
    root = tree.getroot()
    areas = tree.xpath('.//svg:g[@inkscape:label="export-areas"]',namespaces=ns)
    area = areas[0]
    # print(areas)
    # Gather rectangles from SVG, in layer named "export-areas" and its sub-layers. The names of the sub-layers become part of the PDf filenames.
    # Organizes rectangles by layer, and by coordinates from top left to bottom right (So that you don't need to worry about the page order in the SVG)
    for file in area:
        printname = planname+'_'+file.attrib['{'+ns['inkscape']+"}label"]
        print ("Layer "+printname+'.pdf')
        doctitle = printname.capitalize().replace("_", " ")
        # print(doctitle)
        rectangles = []
        pdfcommand = ""
        for i,rect in enumerate(file):
            if "rect" in rect.tag:
                name = rect.attrib['id']

                # This method works only if there are no transforms on the rectangles or their parent groups.
                x = float(rect.attrib['x'])
                y = float(rect.attrib['y'])
                w = float(rect.attrib['width'])
                h = float(rect.attrib['height'])
                
                rectangles.append({'i':i,'x':x, 'y':y, 'w':w, 'h':h,'name':name})
        # Sort rectangles by x,y, coordinates (first y, then x)
        rectangles.sort(key=lambda r: r['y']*10000+r['x'])
        # print(rectangles)
        
        # Export PDFs from inkscape
        for i,rect in enumerate(rectangles):
            
            
        
            rectname = targetdir+"\\"+printname+str(i+1)+'.pdf'
            # add to pdf merge command file text
            pdfcommand += curdir+"\\"+targetdir+"\\"+printname+str(i+1)+'.pdf;1;include\n'
            # Only export the file if overwrite is on and the file doesn't exist
            exists = os.path.isfile(rectname)
            if not exists or (exists and overwrite):
                print(rectname)
                # Move everything in drawing to position current rectangle inside the page
                # Margin is (A4 page size - rectangle size) / 2
                marginx = (210.0-rect['w']) / 2.0
                marginy = (297.0-rect['h']) / 2.0
                # Add transform to lowest layer groups, since it doesn't do anything on the root svg node
                transform = 'translate(%.2f, %.2f)' % (-rect['x']+marginx, -rect['y']+marginy)
                print(transform)
                tree = etree.parse(tempfile)
                root = tree.getroot()
                layers = root.findall('svg:g',ns)
                for layer in layers:
                    layer.set("transform",transform)
                tree.write(tempfile)
                # Export PDF
                command = 'inkscape --export-pdf="%s" "%s"' % (rectname, tempfile)
                subprocess.Popen(command, shell=False, stdout=subprocess.PIPE).stdout.read()
                # .stdout.read() waits for inkscape to finish each time; Otherwise pdfmerge would not have enough files to work on.
           


        # finally merge pdfs with PDFMerge command line
        # TODO: It would be better to use the XML file format for the PDFMerge command file, since it has more options.
        # Add document metadata to pdf command
        # doctitle here is used as the title of the PDF file
        pdfcommand += '[Info];%s;%s' % (doctitle, "subject field")
        print(pdfcommand)
        # Create a PDFMerge command document(s)
        pdfcommandfile = curdir+"\\"+targetdir+"\\"+printname+'.txt'
        with open(pdfcommandfile, 'w') as file:
            file.write(pdfcommand)
        # Merge PDFs
        command = '"%s" "%s" "%s"' % (pdfmergepath, pdfcommandfile, curdir+"\\"+targetdir+"\\"+printname+'.pdf')
        subprocess.Popen(command, shell=False, stdout=subprocess.PIPE).stdout.read() 

    print ("done!")      
    
    
    
    

# Run module as script      
if __name__ == "__main__":
    import sys
    export(sys.argv[0], bool(sys.argv[1]))









