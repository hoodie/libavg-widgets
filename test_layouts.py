#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import libavg
from libavg     import avg, app, player

import widgets
from widgets import VLayout, HLayout, Layout, GridLayout, DivNodePlus, Orientation

def rect(color, text = None,size = (60,60)):
    div  = DivNodePlus()
    rect = libavg.RectNode( size = size, opacity = 0, fillopacity = 1, fillcolor = color)
    div.appendChild(rect)

    if not text == None:
        words = avg.WordsNode(pos = (0,0), color="000000", text=text, fontsize = 45, alignment="left", parent = div)
        return div
    else:
        return rect

# BaseWidget
#   fillParent
#   fillParentV
#   fillParentH
#   snapToParentTop...

def puts(stuff):
    print stuff

class MainDiv(app.MainDiv):
    def onInit(self):
        self.mainlayout = VLayout()
        self.appendChild(self.mainlayout)
        self.buildGrid()
        self.buildLayouts()
        

    def buildGrid(self):
        grid = GridLayout(rows=4,background = rect("aaaaaa"))
        grid.subscribe(grid.RENDERED, lambda stuff: puts("grid.size: {0}".format(grid.size)))

        grid.appendChild(rect("aa0000", "0"))
        grid.appendChild(rect("ff0000", "1"))
        grid.appendChild(rect("fff000", "2"))
        grid.appendChild(rect("00ff00", "3"))
        grid.appendChild(rect("00fff0", "4"))
        grid.appendChild(rect("0000ff", "5"))
        grid.appendChild(rect("0000aa", "6"))
        grid.appendChild(rect("aa0000", "7"))
        grid.appendChild(rect("ff0000", "8"))
        grid.appendChild(rect("fff000", "9"))
        grid.appendChild(rect("00ff00", "10"))
        grid.appendChild(rect("00fff0", "11"))
        grid.appendChild(rect("0000ff", "12"))
        grid.appendChild(rect("0000aa", "13"))

        self.mainlayout.appendChild(grid)
        print "size before scale:", grid.size
        grid.scale(1.5)
        print "size after scale:", grid.size
        self.appendChild(libavg.RectNode(pos = grid.pos, size = grid.size, color = "ff0000"))
        dot = libavg.RectNode(fillcolor = "ff0000", fillopacity=1, opacity=0, size = (5,5))
        dot.pos = grid.size
        self.appendChild(dot)

    def buildLayouts(self):
        # 1 4
        # 2 5
        # 3 6
        vlayout0 = widgets.VLayout(background = rect("333333"))
        vlayout0.appendChild(rect("FF0000", "1")); vlayout0.appendChild(rect("00FF00", "2")); vlayout0.appendChild(rect("0000FF", "3"))
        vlayout1 = widgets.VLayout(background = rect("333333"))
        vlayout1.appendChild(rect("00FFFF", "4")); vlayout1.appendChild(rect("FF00FF", "5")); vlayout1.appendChild(rect("FFFF00", "6"))
        hlayout0 = widgets.HLayout(background = rect("555555"))

        # 7 8 9
        hlayout1 = widgets.HLayout(background = rect("333333"))
        hlayout1.appendChild(rect("0044ff", "7")); hlayout1.appendChild(rect("0066ff", "8")); hlayout1.appendChild(rect("0088ff", "9"))

        hlayout0.appendChild(vlayout0); hlayout0.appendChild(vlayout1); hlayout0.appendChild(hlayout1)
        
        self.mainlayout.appendChild(hlayout0)

        grid = GridLayout(rows= 2,background = rect("333333"))
        grid.appendChild(rect("FFFF99", "1")); grid.appendChild(rect("FFFFAA", "2")); grid.appendChild(rect("FFFFBB", "3")); grid.appendChild(rect("FFFFDD", "4")); grid.appendChild(rect("FFFFFF", "5"));
        grid.appendChild(rect("DDDD99", "6")); grid.appendChild(rect("DDDDAA", "7")); grid.appendChild(rect("DDDDBB", "8")); grid.appendChild(rect("DDDDDD", "9")); grid.appendChild(rect("DDDDFF", "10"));
        self.mainlayout.appendChild(grid)


        grid = GridLayout(rows= 2,background = rect("333333"))
        grid.appendChild(rect("FFFF99", "1")); grid.appendChild(rect("FFFFAA", "2")); grid.appendChild(rect("FFFFBB", "3")); grid.appendChild(rect("FFFFDD", "4")); grid.appendChild(rect("FFFFFF", "5"));
        grid.appendChild(rect("DDDD99", "6")); grid.appendChild(rect("DDDDAA", "7")); grid.appendChild(rect("DDDDBB", "8")); grid.appendChild(rect("DDDDDD", "9")); grid.appendChild(rect("DDDDFF", "10"));
        grid.scale(1.1)
        self.mainlayout.appendChild(grid)


        layout = Layout(Orientation.HORIZONTAL)
        layout.appendChild(rect("FFFF99", "1"))
        layout.appendChild(rect("FFFFAA", "2"))
        layout.appendChild(rect("FFFFBB", "3"))
        layout.appendChild(rect("FFFFDD", "4"))
        layout.appendChild(rect("FFFFFF", "5"))
        self.mainlayout.appendChild(layout)



    def onStartup(self):
        print "onStartup"

    def onExit(self):
        pass

    def onFrame(self): # TODO https://www.libavg.de/site/projects/libavg/wiki/App sais onFrame(self,delta)
        pass

    def onArgvParserCreated(self, parser):
        parser.add_option('--speed', '-s', default='0.3', dest='speed',
                help='Pixels per second')
        parser.add_option('--color', '-c', default='ff0000', dest='color',
                help='Fill color of the running block')

    # This method is called when the command line options are being parsed.
    # options, args are the result of OptionParser.parse_args().
    def onArgvParsed(self, options, args, parser):
        self.argvoptions = options

    
app.App().run(MainDiv(), app_resolution="612x792")
