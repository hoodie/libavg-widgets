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
