#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import libavg
from libavg     import avg, app, player

import widgets
from widgets import VLayout, HLayout, Layout, GridLayout, DivNodePlus, Orientation, Label

def rect(color, text = None,size = (60,60)):
    div  = DivNodePlus()
    rect = libavg.RectNode( size = size, opacity = 0, fillopacity = 1, fillcolor = color)
    div.appendChild(rect)

    if not text == None:
        words = libavg.WordsNode(pos = (0,0), color="000000", text=text, fontsize = 45, alignment="left", parent = div)
        return div
    else:
        return rect

def mixedWidthGrid(cols=3, orientation = Orientation.HORIZONTAL):
    div = DivNodePlus()
    grid = GridLayout(cols=cols,background = rect("aaaaaa"), orientation = orientation)
    #grid.subscribe(grid.RENDERED, lambda stuff: print("grid.size: {0}".format(grid.size)))

    grid.appendChild(rect("ff0000", "1", (60,60)))
    grid.appendChild(rect("00ff00", "2", (60,80)))
    grid.appendChild(rect("0000ff", "3", (60,60)))
    grid.appendChild(rect("aa0000", "4", (80,60)))
    grid.appendChild(rect("00aa00", "5", (60,60)))
    grid.appendChild(rect("0000aa", "6", (60,60)))
    grid.appendChild(rect("660000", "7", (60,60)))
    grid.appendChild(rect("006600", "8", (60,60)))
    grid.appendChild(rect("000066", "9", (60,60)))

    div.appendChild(grid)
    div.appendChild(libavg.RectNode(pos = grid.pos, size = grid.size, color = "ff0000"))
    dot = libavg.RectNode(fillcolor = "ff0000", fillopacity=1, opacity=0, size = (5,5))
    dot.pos = grid.size
    div.appendChild(dot)

    return div

def mixedWidthTab(cols=3, orientation = Orientation.HORIZONTAL):
    div = DivNodePlus()
    grid = GridLayout(
            cols=cols,
            background = rect("aaaaaa"),
            orientation = orientation,
            tabular = True
            )
    #grid.subscribe(grid.RENDERED, lambda stuff: print("grid.size: {0}".format(grid.size)))

    grid.appendChild(rect("ff0000", "1", (60,60)))
    grid.appendChild(rect("00ff00", "2", (60,80)))
    grid.appendChild(rect("0000ff", "3", (60,60)))
    grid.appendChild(rect("aa0000", "4", (80,60)))
    grid.appendChild(rect("00aa00", "5", (60,60)))
    grid.appendChild(rect("0000aa", "6", (60,60)))
    grid.appendChild(rect("660000", "7", (60,60)))
    grid.appendChild(rect("006600", "8", (60,60)))
    grid.appendChild(rect("000066", "9", (60,60)))

    div.appendChild(grid)
    div.appendChild(libavg.RectNode(pos = grid.pos, size = grid.size, color = "ff0000"))

    dot = libavg.RectNode(fillcolor = "ff0000", fillopacity=1, opacity=0, size = (5,5))
    dot.pos = grid.size
    div.appendChild(dot)

    return div

class MainDiv(app.MainDiv):
    def onInit(self):
        mainlayout = GridLayout(rows=3, orientation=Orientation.VERTICAL)
        self.appendChild(mainlayout)

        grid_vert = mixedWidthGrid(orientation=Orientation.VERTICAL)
        grid_hori = mixedWidthGrid(orientation=Orientation.HORIZONTAL)
        tab_vert  = mixedWidthTab(orientation=Orientation.VERTICAL)
        tab_hori  = mixedWidthTab(orientation=Orientation.HORIZONTAL)

        mainlayout.appendChild(Label("grid layout", color="FFFFFF"))
        mainlayout.appendChild( grid_vert )
        mainlayout.appendChild( grid_hori )

        mainlayout.appendChild(Label("tabular layout", color="FFFFFF"))
        mainlayout.appendChild( tab_vert )
        mainlayout.appendChild( tab_hori )


app.App().run(MainDiv(), app_resolution="1000x700")
