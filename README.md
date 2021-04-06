# houdini_axidraw_plot

Houdini Digital Asset, wrapper for AxiDraw Python API which provides most of available functionalities and print polygon lines (in XY plane) straight to the plotter. The HDA assumes the line drawing in the XY plane, with inverted Y so the plotter's HOME is top left together with Houdini's grid origin. The node previews the chosen page dimensions which can be traced together with the bounding box of the design.



## Installation
Houdini 18.5 running Python3.7 . By default houdini ship with Python2.7 so you may need to instal the appropriate build.
https://www.sidefx.com/download/daily-builds/

Using pip instal the latest Axidraw API.
`pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip`


svgwrite is also used
`pip install svgwrite`


