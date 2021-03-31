from axidrawinternal import axidraw
import svgwrite
from svgwrite import cm, inch


hda = hou.pwd()
geo = hda.node('IN').geometry()
prims = geo.prims()

   

def geo2svg():
    print('--------------------')
    svg_out = hou.parm('svg_out').evalAsString()
    unitsPar = hou.parm('units').evalAsInt()
    sizeX = hou.parmTuple('size').eval()[0]
    sizeY = hou.parmTuple('size').eval()[1]
    
    
    un = ''
    if unitsPar == 0 :
        un = 'cm'
    elif unitsPar == 1 :
        un = 'in'

    
    sXstr = str(sizeX)+un
    
    svg = svgwrite.Drawing(
        filename=svg_out,
        size=(str(sizeX)+un, str(sizeY)+un), viewBox=('0 0 '+str(sizeX)+' '+str(sizeY) )
    )
    
    

    for pr in range(0, len(prims)):
        # path = svg.add(svg.g(id='path_', stroke='black'))
        vertices = prims[pr].vertices()
        
        #check for empty primitives
        if len(vertices) == 0:
            continue;

        points = []
        for v in range(0, len(vertices)):
            pt = vertices[v].point()
            pos = pt.position()

            x = str( pos[0] )
            y = str( -pos[1] )
            points.append( (x,y) )

        path = svg.add(svg.polyline( points, stroke_width=0.02, stroke='black', fill='none'))

  
    return svg;









def plot():

    svg = geo2svg()

    ad = axidraw.AxiDraw()             # Create class instance
    ad.plot_setup(svg.tostring())    # Parse the SVG 
    ad.options.speed_pendown = 110 # Set maximum pen-down speed to 50%
    ad.options.speed_penup = 110 # Set maximum pen-down speed to 50%
    ad.plot_run()   # plot the document
    



    
def save():
        geo2svg().save()
        print('Saved SVG')
    
    

def test():
    print('ok')
    print(geo)