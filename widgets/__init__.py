import math, os, widget_config
import libavg

from libavg import avg, geom, widget as avg_widget
from libavg.widget import Orientation

from skin       import initSkin
from layout     import Layout, HLayout, VLayout, GridLayout
from widgetbase import WidgetBase
from bars       import ButtonBar, ToggleButtonBar
from buttons    import Button, ToggleButton, buttonImg, ButtonBackground
from sliders    import Slider, StepSlider
from switch     import SwitchSlider

SKIN = initSkin()

#[deprecated]
def Separator(width = widget_config.ICON_SIZE, height = widget_config.ICON_SIZE / 20, fillcolor = "808080"):
    return avg.RectNode( size = (width, height),
            color = fillcolor, opacity = 0, fillcolor = fillcolor, fillopacity = 1)

#[deprecated]
def VSeparator(width = widget_config.ICON_SIZE/20, height = widget_config.ICON_SIZE, fillcolor = "808080"):
    return avg.RectNode( size = (width, height),
            color = fillcolor, opacity = 0, fillcolor = fillcolor, fillopacity = 1)

def LayoutBackground(color, size= (0, 0), opacity = 1):
    return libavg.geom.RoundedRect(
        size, 0, (0, 0),
        color       = color, opacity     = opacity,
        fillcolor   = color, fillopacity = opacity)

#[deprecated]
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
