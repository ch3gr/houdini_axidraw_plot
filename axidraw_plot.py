# https://axidraw.com/doc/py_api/#
# from axidrawinternal import axidraw   # This used to work, but not any more
from pyaxidraw import axidraw
import svgwrite
from svgwrite import cm, inch

# Create AxiDraw
ad = axidraw.AxiDraw()
ad.plot_setup()

svgResume = None

def pagePresetToCustom():
    hou.parm('preset').set(0)

def pagePresets():

    unitsPar = hou.parm('units').evalAsInt()
    preset = hou.parm('preset').evalAsInt()

    if preset == 0 :
        return

    # A3 Landscape
    if preset == 1:
        sizeX = 420
        sizeY = 297
    # A4 Portrait
    if preset == 2:
        sizeX = 210
        sizeY = 297
    # A4 Landscape
    if preset == 3:
        sizeX = 297
        sizeY = 210
    # A5 Portrait
    if preset == 4:
        sizeX = 148
        sizeY = 210        
    # A5 Landscape
    if preset == 5:
        sizeX = 210
        sizeY = 148
        
    if unitsPar == 0 :
        sizeX *= 0.0393701
        sizeY *= 0.0393701
    if unitsPar == 1 :
        sizeX *= 0.1
        sizeY *= 0.1
        
    hou.parm('sizex').set(sizeX)
    hou.parm('sizey').set(sizeY)


    
    
def geo2svg( geo ):
    hda = hou.pwd()
    geo = hda.node(geo).geometry()
    prims = geo.prims()

    svg_out = hou.parm('svg_out').evalAsString()
    unitsPar = hou.parm('units').evalAsInt()
    
    pagePresets()

    sizeX = hou.parmTuple('size').eval()[0]
    sizeY = hou.parmTuple('size').eval()[1]
    
    un = ''
    if unitsPar == 0 :
        un = 'in'
    elif unitsPar == 1 :
        un = 'cm'
    elif unitsPar == 2 :
        un = 'mm'

        
        
    svg = svgwrite.Drawing(
        filename=svg_out,
        size=(str(sizeX)+un, str(sizeY)+un), viewBox=('0 0 '+str(sizeX)+' '+str(sizeY) )
    )
    #############
    

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




def updateOptions():
    global ad
    
    # OPTIONS
    ad.options.units = hou.parm('units').evalAsInt()
    
    ad.options.speed_pendown = hou.parm('speed_pendown').evalAsInt()
    ad.options.speed_penup = hou.parm('speed_penup').evalAsInt()
    ad.options.accel = hou.parm('accel').evalAsInt()
    ad.options.pen_pos_down = hou.parm('pen_pos_down').evalAsInt()
    ad.options.pen_pos_up = hou.parm('pen_pos_up').evalAsInt()

    ad.options.pen_rate_lower = hou.parm('pen_rate_lower').evalAsInt()
    ad.options.pen_rate_raise = hou.parm('pen_rate_raise').evalAsInt()

    ad.options.pen_delay_down = hou.parm('pen_delay_down').evalAsInt()
    ad.options.pen_delay_up = hou.parm('pen_delay_up').evalAsInt()
    
    ad.options.const_speed = hou.parm('const_speed').evalAsInt()
    
    ad.options.model = hou.parm('model').evalAsInt() + 1
    
    ad.options.auto_rotate = False
    ad.options.report_time = hou.parm('info').evalAsInt()
    


    
def trace( square ):
    global ad
    
    if square == 0:
        svg = geo2svg('PAGE')
    if square == 1:
        svg = geo2svg('BOUNDS')

    ad.plot_setup(svg.tostring())    # Parse the SVG
    ad.options.mode = "plot"
    updateOptions()    
    
    ad.options.speed_pendown = 110
    ad.options.speed_penup = 110
    ad.options.pen_pos_down = hou.parm('pen_pos_up').evalAsInt()
    ad.options.pen_pos_up = hou.parm('pen_pos_up').evalAsInt()

    ad.options.pen_rate_lower = 100
    ad.options.pen_rate_raise = 100
    ad.options.pen_delay_down = 0
    ad.options.pen_delay_up = 0
   
    #PLOT
    ad.plot_run()
    return
    

    
    
def plot():
    global ad
    global svgResume
        
    svg = geo2svg('GEO')
    ad.plot_setup(svg.tostring())    # Parse the SVG
    ad.options.mode = "plot"

    updateOptions()    
   
    #PLOT
    svgResume = ad.plot_run(True)
    


def align():
    global ad
    ad.plot_setup()
    updateOptions()
    ad.options.mode = "align"
    ad.plot_run()
    print('Axidraw_Plot: Motors Off')
    
def toggle():
    # print('Axidraw_Plot: Toggle')
    global ad
    # ad = axidraw.AxiDraw()
    print( ad )
    ad.plot_setup()
    updateOptions()
    ad.options.mode = "toggle"
    ad.plot_run()

    print( ad )




def up():
    # print('Axidraw_Plot: Toggle')
    global ad
    # ad = axidraw.AxiDraw()
    print( ad )
    ad.plot_setup()
    updateOptions()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "raise_pen"
    ad.plot_run()

    print( ad )

def down():
    # print('Axidraw_Plot: Toggle')
    global ad
    # ad = axidraw.AxiDraw()
    print( ad )
    ad.plot_setup()
    updateOptions()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "lower_pen"
    ad.plot_run()

    print( ad )



def home():
    global svgResume
    if( svgResume != None ):
        global ad
        ad.plot_setup(svgResume)
        updateOptions()
        ad.options.mode = "res_home"
        print('Axidraw_Plot: Home')
        ad.plot_run()
        svgResume = None
    else:
        print('Axidraw_Plot: No plotter resume data')

def resume():
    global svgResume
    if( svgResume != None ):
        global ad
        ad.plot_setup(svgResume)
        updateOptions()
        ad.options.mode = "res_plot"
        print('Axidraw_Plot: Resume')
        ad.plot_run(True)
        svgResume = None
    else:
        print('Axidraw_Plot: No plotter resume data')
    
def save():
        geo2svg('GEO').save()
        print("Axidraw_Plot: SVG saved > " + hou.parm('svg_out').evalAsString())
    
    

def estimate():
    print("\n")
    global ad
    svg = geo2svg('GEO')
    ad.plot_setup(svg.tostring())    # Parse the SVG
    updateOptions()
    
    ad.options.preview=1
    ad.options.report_time = 1
    ad.plot_run()
    
def test():
    print('Axidraw_Plot: Test')
    global ad
    ad = axidraw.AxiDraw()
    print( ad )
    ad.plot_setup()
    ad.options.mode = "sysinfo"
    ad.plot_run()
    print('<<<  <<<<')
    