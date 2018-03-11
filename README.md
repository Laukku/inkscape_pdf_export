# inkscape_pdf_export

Export multiple PDF pages from Inkscape. Merge PDF pages into one file or more. Easily mark areas to be exported with rectangles. 

The idea for this script came from trying to automate printing from Inkscape. It is only possible to export the page area with the command line. This script works by moving everything in the SVG file so that the areas you want to print are on the page.

## Getting Started

Put inkscape_pdf_export.py somewhere - this file is a module that contains most of the code. Put an export.py in the same directory as you SVG file. This is a short config file.

### Prerequisites

This script was written for python 3. This module uses lxml to read SVG files. An external program called PdfMerge is required for combining exported PDF pages into larger documents. Get it from https://www.pdfmerge.com/

```
pip install lxml
```

### Structuring your SVG file
Create a layer called "export-areas". Don't put any rectangles here. Then create as many sub-layers as you want output files; Each sublayer ends up as a PDF document, and the layer name is used as part of the filename. In these sublayers, create rectangle objects, one for each PDF page. These don't need to be named. They will be automatically sorted by their y and x coordinates, from top left to bottom right. Hide the "export-areas" layer if you don't want to see the rectangles in the PDFs. They will be centered on the page.

Additionally, everything else in the SVG file must be inside layers; It's sometimes possible to have some elements outside of a layer, especially if the SVG file was created outside of Inkscape.

View example.svg for an example. 

### config file export.py
Put this file in the same directory as your SVG file. 
```
# Config script for inkscape_pdf_export
import sys, os
# Temporarily add directory where inkscape_pdf_export module is located to system path so it can be imported
sys.path.insert(0, r'C:\this\is\where\I\keep\my\module')
import inkscape_pdf_export

curdir = os.getcwd() # Location of this python script, which is assumed to be in the same folder as the SVG file
SVGfile = "MySVGfile.svg" # SVG file to be sliced into PDFs
# Run:
inkscape_pdf_export.export(curdir+"\\"+SVGfile, overwrite=True)
```
Finally run the script:
```
python export.py
```

## Authors

* **Lauri Niskanen** - *Initial work* - [Niskanen Lutes](https://www.niskanenlutes.com)


## License

Permission is given to use this script for whatever purpose. No promise of usefullness or suitability for any purpose is given.
