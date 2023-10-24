# houdini_axidraw_plot

Houdini Digital Asset, a wrapper for AxiDraw Python API which provides most of the available functionalities. It allows printing to the plotter straight from houdini, without exporting an .svg file or using inkscape at all. The HDA recognises polygonal lines and assumes the drawing is on the XY plane, with inverted Y so the plotter's HOME corresponds to Houdini's top left grid origin. The node previews the chosen page size which can also be traced with the pen up together with the bounding box of the drawing to ensure it fits the paper.

The HDA is made using Houdini's indie license and it will most likely downgrade your session if you are using the full license.


## Installation

Inside Houdini, open a Shell under the Windows menu and use these commands to install:  
`hython -m pip install svgwrite`  
`hython -m pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip`  

Tested and works in Houdini 19.5

If you use Houdini 18 or older, make sure you have a Python3.7 build. By default houdini 18 ship with Python2.7 so you may need to instal the appropriate build.
https://www.sidefx.com/download/daily-builds/  

You can also install the two python libraries manually. These are not provided in this repo, so please read their respective licenses.  

**The latest Axidraw API**  
https://github.com/evil-mad/axidraw

**svgwrite**  
https://github.com/mozman/svgwrite/





