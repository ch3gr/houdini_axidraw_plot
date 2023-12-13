# https://axidraw.com/doc/py_api/#
# from axidrawinternal import axidraw   # This used to work, but not any more
from pyaxidraw import axidraw
import svgwrite
from svgwrite import cm, inch

# Create AxiDraw
# ad = axidraw.AxiDraw()
# ad.plot_setup()

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
        sizeY = 296
    # A4 Portrait
    if preset == 2:
        sizeX = 210
        sizeY = 296
    # A4 Landscape
    if preset == 3:
        sizeX = 296
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






def updateOptions(ad):
    # global ad
    
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
    ad.options.penlift = hou.parm('servo').evalAsInt() + 1
    
    ad.options.auto_rotate = False
    ad.options.report_time = hou.parm('verbose').evalAsInt()

    return ad
    




    
def trace( square ):
    # global ad
    
    if square == 0:
        svg = geo2svg('PAGE')
    if square == 1:
        svg = geo2svg('BOUNDS')

    ad = axidraw.AxiDraw()
    ad.plot_setup(svg.tostring())    # Parse the SVG
    ad.options.mode = "plot"
    ad = updateOptions(ad)
    
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
    


    
def markCorners():
    # global ad

    svg = geo2svg('CORNERS')

    ad = axidraw.AxiDraw()
    ad.plot_setup(svg.tostring())    # Parse the SVG
    ad.options.mode = "plot"
    ad = updateOptions(ad)
    
    # ad.options.speed_pendown = 50
    # ad.options.speed_penup = 110
    # ad.options.pen_pos_down = hou.parm('pen_pos_up').evalAsInt()
    # ad.options.pen_pos_up = hou.parm('pen_pos_up').evalAsInt()

    # ad.options.pen_rate_lower = 100
    # ad.options.pen_rate_raise = 100
    # ad.options.pen_delay_down = 0
    # ad.options.pen_delay_up = 0
   
    #PLOT
    ad.plot_run()
    return
    

    

    
def plot():
    # global ad
    global svgResume
        
    svg = geo2svg('GEO')

    ad = axidraw.AxiDraw()
    ad.plot_setup(svg.tostring())    # Parse the SVG
    ad = updateOptions(ad)
    ad.options.mode = "plot"
   
    #PLOT
    svgResume = ad.plot_run(True)
    



def align():
    if hou.node(".").parm('verbose').eval() :
        print('Axidraw_Plot: Motors Off')

    # global ad
    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad = updateOptions(ad)
    ad.options.mode = "align"
    ad.plot_run()
    

def toggle():
    if hou.node(".").parm('verbose').eval() :
        print('Axidraw_Plot: Toggle')

    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad = updateOptions(ad)
    ad.options.pen_rate_lower = 100
    ad.options.pen_rate_raise = 100
    # ad.options.pen_pos_down = hou.parm('pen_pos_down').evalAsInt()
    # ad.options.pen_pos_up = hou.parm('pen_pos_up').evalAsInt()
    ad.options.mode = "toggle"
    print(ad)
    
    ad.plot_run()



def tog():

    ad_temp = axidraw.AxiDraw()
    ad_temp.plot_setup()
    updateOptions()
    ad_temp.options.pen_rate_lower = 100
    ad_temp.options.pen_rate_raise = 100
    ad_temp.options.pen_pos_down = 30
    ad_temp.options.pen_pos_up = 90
    ad_temp.options.mode = "toggle"
    print(ad_temp)
    
    ad_temp.plot_run()





def up():
    if hou.node(".").parm('verbose').eval() :
        print('Axidraw_Plot: Up')

    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad = updateOptions(ad)
    ad.options.mode = "manual"
    ad.options.manual_cmd = "raise_pen"
    ad.plot_run()


def down():
    if hou.node(".").parm('verbose').eval() :
        print('Axidraw_Plot: Down')

    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad = updateOptions(ad)
    ad.options.mode = "manual"
    ad.options.manual_cmd = "lower_pen"
    ad.plot_run()



def home():
    global svgResume
    if( svgResume != None ):
        if hou.node(".").parm('verbose').eval() :
            print('Axidraw_Plot: Home')

        # global ad
        ad = axidraw.AxiDraw()
        ad.plot_setup(svgResume)
        ad = updateOptions(ad)
        ad.options.mode = "res_home"
        ad.plot_run()
        svgResume = None
    else:
        if hou.node(".").parm('verbose').eval() :
            print('Axidraw_Plot: No plotter resume data')

def resume():
    global svgResume
    if( svgResume != None ):
        if hou.node(".").parm('verbose').eval() :
            print('Axidraw_Plot: Resume')

        # global ad
        ad = axidraw.AxiDraw()
        ad.plot_setup(svgResume)
        ad = updateOptions(ad)
        ad.options.mode = "res_plot"
        ad.plot_run(True)
        svgResume = None
    else:
        if hou.node(".").parm('verbose').eval() :
            print('Axidraw_Plot: No plotter resume data')
    

def save():
        geo2svg('GEO').save()
        print("Axidraw_Plot: SVG saved > " + hou.parm('svg_out').evalAsString())
    
    

def estimate():
    print("\n")
    print('Axidraw_Plot: ')
    # global ad
    svg = geo2svg('GEO')
    ad = axidraw.AxiDraw()
    ad.plot_setup(svg.tostring())    # Parse the SVG
    ad = updateOptions(ad)
    
    ad.options.preview=1
    ad.options.report_time = 1
    ad.plot_run()


def printInfo():
    print('Axidraw_Plot: Info')
    # global ad
    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad.options.mode = "sysinfo"
    ad.plot_run()
    print('')
    

    
def test():
    print('Axidraw_Plot: Test')
    # global ad
    # print( ad )
    
    # print( hou.node("..").parm('verbose').eval()  )
    # print( hou.node(".").parm('verbose').eval() )
    print('_____')
    