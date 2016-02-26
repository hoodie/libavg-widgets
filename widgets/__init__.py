from widget      import BaseWidget
from layout      import Layout, HLayout, VLayout, GridLayout
from layout      import Orientation
from divnodeplus import DivNodePlus
from bars        import ButtonBar, ToggleButtonBar
from buttons     import Button, ToggleButton, buttonImg, ButtonBackground

import math, os, widget_config
import libavg
from libavg    import avg, widget as avg_widget
import libavg.geom
avg.geom = libavg.geom

def initSkin():
    pwdPath = os.path.dirname(os.path.realpath(__file__))
    mediaPath = os.path.join(pwdPath, "skin")
    return avg_widget.Skin("CustomSkin.xml", mediaPath)

SKIN = initSkin()

def Separator(width = widget_config.ICON_SIZE, height = widget_config.ICON_SIZE/20,fillcolor = "808080"):
    return avg.RectNode( size = (width, height),
            color = fillcolor, opacity = 0, fillcolor = fillcolor, fillopacity = 1)

def VSeparator(width = widget_config.ICON_SIZE/20, height = widget_config.ICON_SIZE,fillcolor = "808080"):
    return avg.RectNode( size = (width, height),
            color = fillcolor, opacity = 0, fillcolor = fillcolor, fillopacity = 1)


def LayoutBackground(color, size= (0,0), opacity = 1):
    return avg.geom.RoundedRect(
        size, 0, (0, 0),
        color       = color, opacity     = opacity,
        fillcolor   = color, fillopacity = opacity)

def Slider(onPressed = None, onChanged = None, size = 650, thumbPos = 0.5):
    slider          = avg_widget.Slider(skinObj = SKIN)
    slider.size     = avg.Point2D(size,80)
    slider.thumbPos = thumbPos

    if onChanged:
        slider.subscribe(avg_widget.Slider.THUMB_POS_CHANGED, onChanged)
    if onPressed:
        slider.subscribe(avg_widget.Slider.PRESSED, onPressed)
    return slider

def Label(string, color="000000", size=20):
    return avg.WordsNode(text = string, color=color, fontsize=size)

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
