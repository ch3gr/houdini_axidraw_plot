# houdini_axidraw_plot

Houdini Digital Asset, a wrapper for AxiDraw Python API which provides most of the available functionalities. It allows printing to the plotter straight from houdini, without exporting an .svg file or using inkscape at all. The HDA recognises polygonal lines and assumes the drawing is on the XY plane, with inverted Y so the plotter's HOME corresponds to Houdini's top left grid origin. The node previews the chosen page size which can also be traced with the pen up together with the bounding box of the drawing to ensure it fits the paper.

The HDA is made using Houdini's indie license and it will most likely downgrade your session if you are using the full license.


## Installation
You will need Houdini 18.5 running Python3.7 . By default houdini ship with Python2.7 so you may need to instal the appropriate build.
https://www.sidefx.com/download/daily-builds/


You will also have to install the two python libraries below, either using PIP or manually. These are not provided in this repo, so please read their respective licenses.

The latest Axidraw API:
`pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip`
https://github.com/evil-mad/axidraw


svgwrite:
`pip install svgwrite`
https://github.com/mozman/svgwrite/



## To DO

- Add goto functionality to allow accurate registration of multi page prints.
- Spawn a seperate process while printing, so houdini doesn't freeze.
