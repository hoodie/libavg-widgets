from widget      import BaseWidget
from layout      import Layout, HLayout, VLayout, GridLayout
from layout      import Orientation
from divnodeplus import DivNodePlus
from bars        import ButtonBar, ToggleButtonBar

import math, os, widget_config
import libavg
from libavg    import avg, widget
import libavg.geom
avg.geom = libavg.geom

def initSkin():
    pwdPath = os.path.dirname(os.path.realpath(__file__))
    mediaPath = os.path.join(pwdPath, "skin")
    return libavg.widget.Skin("CustomSkin.xml", mediaPath)

SKIN = initSkin()

def Separator(width = widget_config.ICON_SIZE, height = widget_config.ICON_SIZE/20,fillcolor = "808080"):
    return avg.RectNode( size = (width, height),
            color = fillcolor, opacity = 0, fillcolor = fillcolor, fillopacity = 1)

def VSeparator(width = widget_config.ICON_SIZE/20, height = widget_config.ICON_SIZE,fillcolor = "808080"):
    return avg.RectNode( size = (width, height),
            color = fillcolor, opacity = 0, fillcolor = fillcolor, fillopacity = 1)


def buttonImg(svgId, size= widget_config.ICON_SIZE):
    svg     = avg.SVG(widget_config.SKIN_SVG_PATH)
    bitmap  = svg.renderElement(svgId,size/widget_config.DPI)
    img     = avg.ImageNode()
    img.setBitmap(bitmap)
    img.pos = avg.Point2D(size/2,size/2) - bitmap.getSize()/2
    return img

def ButtonBackground(color, size = widget_config.ICON_SIZE, opacity = 1):
    return avg.RectNode( size = (size,size),
            color = color, opacity = 0, fillcolor = color, fillopacity = 1)
    #return avg.geom.RoundedRect(
    #    (size-2, size-2),
    #    size/5, (0, 0),
    #    color       = color, opacity     = opacity,
    #    fillcolor   = color, fillopacity = opacity)

def LayoutBackground(color, size= (0,0), opacity = 1):
    return avg.geom.RoundedRect(
        size, 0, (0, 0),
        color       = color, opacity     = opacity,
        fillcolor   = color, fillopacity = opacity)

def Button(svgId, color="c0c0c0", downcolor = "a0a0a0", opacity = .5, tag = None, onPressed = None, size=widget_config.ICON_SIZE, **kwargs):
    upcolor = color
    up      = avg.DivNode()
    down    = avg.DivNode()
    #up.appendChild(ButtonBackground(upcolor, opacity = opacity, size = size))
    up.appendChild(buttonImg(svgId, size = size))
    down.appendChild(ButtonBackground(downcolor, opacity = opacity, size = size))
    down.appendChild(buttonImg(svgId, size = size))

    btn = widget.Button(up, down, size = (size, size), **kwargs)
    btn.tag = tag

    if onPressed:
        btn.subscribe(widget.Button.PRESSED, onPressed)

    return btn

def ToggleButton(svgId, tag=None, size=widget_config.ICON_SIZE, color= "c0c0c0", opacity = .5,**kwargs):
    up      = avg.DivNode()
    down    = avg.DivNode()

    down.appendChild(ButtonBackground(color=color, size=size, opacity=opacity))
    up.appendChild(buttonImg(svgId,size))
    down.appendChild(buttonImg(svgId,size))

    btn = widget.ToggleButton(up, up, down, down, size = (size,size), **kwargs)
    btn.tag = tag
    return btn

def Slider(onPressed = None, onChanged = None, size = 650, thumbPos = 0.5):
    slider          = widget.Slider(skinObj = SKIN)
    slider.size     = avg.Point2D(size,80)
    slider.thumbPos = thumbPos

    if onChanged:
        slider.subscribe(widget.Slider.THUMB_POS_CHANGED, onChanged)
    if onPressed:
        slider.subscribe(widget.Slider.PRESSED, onPressed)
    return slider

def Label(string):
    return avg.WordsNode(text = string, color="000000", fontsize=40)

def keepNodeInRect(node, tl, br):
    tl, br = map(avg.Point2D, [tl, br])
    center = node.pos + node.size/2
    if center.x < tl.x:
        node.pos = (tl.x-node.size.x/2, node.pos.y)
    if center.x > br.x:
        node.pos = (br.x-node.size.x/2, node.pos.y)
    if center.y < tl.y:
        node.pos = (node.pos.x, tl.y-node.size.y/2)
    if center.y > br.y:
        node.pos = (node.pos.x, br.y-node.size.y/2)

class BarChart(avg.DivNode):
    def __init__(self, height=200, width=200, barcount=5, label="unnamed sensor", parent=None, *args, **kwargs):
        super(BarChart, self).__init__(*args, **kwargs)

        self.__label = avg.WordsNode(
                pos=(0,0),
                width=210,
                text=label)

        layout = self.__layout = VLayout()
        bars = self.__bars = HLayout(width=width)

        for i in range(barcount):
            bars.appendChild(
                    avg.RectNode(
                        size=((width/barcount)-2,height),
                        opacity=0,
                        fillopacity=1,
                        fillcolor="FFFF00")
                    )

        layout.appendChild(bars)
        layout.appendChild(self.__label)
        self.appendChild(layout)

        origin = avg.Point2D(100,100)

        color_x = "FF0000"
        color_y = "00FF00"
        color_z = "0000FF"

        self.x_axis = avg.LineNode(
                pos1=origin, pos2=origin,
                strokewidth=2, color=color_x, parent=self)

        self.y_axis = avg.LineNode(
                pos1=origin, pos2=origin,
                strokewidth=2, color=color_y, parent=self)

        self.z_axis = avg.LineNode(
                pos1=origin, pos2=origin,
                strokewidth=2, color=color_z, parent=self)

        self.updateLines(100,100,100)

    def setLabel(self, label):
        self.__label.text = label

    def setVals(self, *v):
        m = 1#max(v)

        for i, child in enumerate(self.__bars.children):
            print v[i]/m
            child.pos = (child.pos.x, 200 - ((v[i]*1.0)/m) * 200)
            child.size = (child.size.x, ((v[i]*1.0)/m) * 200)

    def updateLines(self, x, y, z,angle=0):
        x_angle = math.radians(angle)
        y_angle = math.radians(angle - 120)
        z_angle = math.radians(angle + 120)

        self.x_axis.pos2 = self.x_axis.pos1 + (math.sin(x_angle)*x,math.cos(x_angle)*x)
        self.y_axis.pos2 = self.y_axis.pos1 + (math.sin(y_angle)*y,math.cos(y_angle)*y)
        self.z_axis.pos2 = self.z_axis.pos1 + (math.sin(z_angle)*z,math.cos(z_angle)*z)

class SensorVis(avg.DivNode):
    def __init__(self, height=200, width=200, label="unnamed sensor", parent=None, *args, **kwargs):
        super(SensorVis, self).__init__(*args, **kwargs)
        self.label=label
        origin = avg.Point2D(100,100)

        color_x = "FF0000"
        color_y = "00FF00"
        color_z = "0000FF"

        self.x_axis = avg.LineNode(
                pos1=origin, pos2=origin,
                strokewidth=2, color=color_x, parent=self)

        self.y_axis = avg.LineNode(
                pos1=origin, pos2=origin,
                strokewidth=2, color=color_y, parent=self)

        self.z_axis = avg.LineNode(
                pos1=origin, pos2=origin,
                strokewidth=2, color=color_z, parent=self)

        self.label = avg.WordsNode(
                pos=(0,0),
                width=210,
                text=self.label,
                parent=self)

        self.updateLines(100,100,100)

    def setLabel(self, label):
        self.label.text = label
    def updateLines(self, x, y, z,angle=0):
        x_angle = math.radians(angle)
        y_angle = math.radians(angle - 120)
        z_angle = math.radians(angle + 120)

        self.x_axis.pos2 = self.x_axis.pos1 + (math.sin(x_angle)*x,math.cos(x_angle)*x)
        self.y_axis.pos2 = self.y_axis.pos1 + (math.sin(y_angle)*y,math.cos(y_angle)*y)
        self.z_axis.pos2 = self.z_axis.pos1 + (math.sin(z_angle)*z,math.cos(z_angle)*z)

class RoomWidget(avg.DivNode):

    BOX_COLOR = "FFFF66"
    TAB_COLOR0= "AA3333"
    TAB_COLOR1= "FF6666"
    STROKEWIDTH = 1

    def __init__(self, height=200, width=200, label="unnamed sensor", parent=None, *args, **kwargs):
        super(RoomWidget, self).__init__(*args, **kwargs)
        #tablet = self.projectVerts(self.getTablet())
        self.height = height
        self.width  = width
        self.tablet_w = w = self.width/30
        self.tablet_h = h = self.width/50
        print "WIM: size:", self.size
        print "WIM: tablet size:", (w,h)

        self.__background = avg.RectNode( size = (self.height, self.width),
                                          fillopacity=1,
                                          fillcolor="222222",
                                          parent=self)

        box 	= self.box 	  = self.getBox()

        tablet 	= self.tablet = self.getTablet()
        self.initBox()
        self.updateBox()
        self.initTablet()
        self.updateTablet()


    def initBox(self):
        self.boxLines = [
            avg.LineNode(strokewidth=self.STROKEWIDTH, color=self.BOX_COLOR, parent=self) for _ in range(12)]

    def initTablet(self):
        self.tabletLines = [
            avg.LineNode(strokewidth=self.STROKEWIDTH,   color=self.TAB_COLOR0, parent=self),
            avg.LineNode(strokewidth=self.STROKEWIDTH,   color=self.TAB_COLOR0, parent=self),
            avg.LineNode(strokewidth=self.STROKEWIDTH+2, color=self.TAB_COLOR1, parent=self),
            avg.LineNode(strokewidth=self.STROKEWIDTH,   color=self.TAB_COLOR0, parent=self),
            ]

    def updateTablet(self):
        verts = self.tablet
        verts = self.projectVerts(verts)
        self.tabletLines[0].pos1 = verts[0]
        self.tabletLines[0].pos2 = verts[1]
        self.tabletLines[1].pos1 = verts[1]
        self.tabletLines[1].pos2 = verts[2]
        self.tabletLines[2].pos1 = verts[2]
        self.tabletLines[2].pos2 = verts[3]
        self.tabletLines[3].pos1 = verts[3]
        self.tabletLines[3].pos2 = verts[0]

    def updateBox(self):
        verts = self.box
        verts = self.projectVerts(verts)
        self.boxLines[0].pos1 = verts[0]
        self.boxLines[0].pos2 = verts[1]
        self.boxLines[1].pos1 = verts[1]
        self.boxLines[1].pos2 = verts[3]
        self.boxLines[2].pos1 = verts[0]
        self.boxLines[2].pos2 = verts[2]
        self.boxLines[3].pos1 = verts[2]
        self.boxLines[3].pos2 = verts[3]
        self.boxLines[4].pos1 = verts[4]
        self.boxLines[4].pos2 = verts[5]
        self.boxLines[5].pos1 = verts[5]
        self.boxLines[5].pos2 = verts[7]
        self.boxLines[6].pos1 = verts[4]
        self.boxLines[6].pos2 = verts[6]
        self.boxLines[7].pos1 = verts[6]
        self.boxLines[7].pos2 = verts[7]
        self.boxLines[8].pos1 = verts[0]
        self.boxLines[8].pos2 = verts[4]
        self.boxLines[9].pos1 = verts[1]
        self.boxLines[9].pos2 = verts[5]
        self.boxLines[10].pos1 = verts[2]
        self.boxLines[10].pos2 = verts[6]
        self.boxLines[11].pos1 = verts[3]
        self.boxLines[11].pos2 = verts[7]

    def getTablet(self): #-> [(float,float,float);6]
        w = self.tablet_w
        h = self.tablet_h
        return [ (-w/2, -h/2, 0),
                 ( w/2, -h/2, 0),
                 ( w/2,  h/2, 0),
                 (-w/2,  h/2, 0) ]

    def getBox(self): #-> [(float,float,float);6]
        s = self.width/50
        box = [
                (-s,-s,-s),
                ( s,-s,-s),
                (-s, s,-s),
                ( s, s,-s),

                (-s,-s, s),
                ( s,-s, s),
                (-s, s, s),
                ( s, s, s),
                ]
        return box

    def projectVerts(self,verts): #-> [(float,float);6]
        offset = self.width / 2 ## nach oben links
        depth = .4
        new_verts = []
        dist = 150
        for x,y,z in verts:

            x *= 15
            y *= 15
            z *= 15

            z = z * depth
            new_verts.append((x+z+offset,   y-z+offset))

            #z1 = z * .8
            #z2 = (z+dist)/200.0
            #new_verts.append(( (x+z1)/z2 +offset, (y+z1)/z2 +offset))

            #z = (z+dist)/90.0
            #new_verts.append( (x/z+offset,   y/z+offset))
        return new_verts
