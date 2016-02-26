#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import libavg
from libavg     import avg, app, player, RectNode

import widgets
from widgets import VLayout, HLayout, Layout, GridLayout, DivNodePlus, Orientation
from widgets import ButtonBar, ToggleButtonBar, VLayout, HLayout, Orientation
from widgets import Label


def rect(color, text = None,size = (60,60)):
    div  = DivNodePlus()
    rect = libavg.RectNode( size = size, opacity = 0, fillopacity = 1, fillcolor = color)
    div.appendChild(rect)

    if not text == None:
        words = libavg.WordsNode(pos = (0,0), color="000000", text=text, fontsize = 45, alignment="left", parent = div)
        return div
    else:
        return rect

def fillGrid(grid):
    grid.appendChild(rect("0000FF","1",(100,60)))
    grid.appendChild(rect("0000FF","2",(100,60)))
    grid.appendChild(rect("FF00FF","3",(100,60)))
    grid.appendChild(rect("FF00FF","4",(100,60)))
    grid.appendChild(rect("FF0000","5",(100,60)))
    grid.appendChild(rect("FF0000","6",(100,60)))

    return grid

class MainDiv(app.MainDiv):

    def onInit(self):
        mainlayout = GridLayout(rows=3, orientation = Orientation.VERTICAL)
        self.appendChild(mainlayout)

        grid = GridLayout(cols = 2, tabular=False, orientation=Orientation.VERTICAL)
        grid = fillGrid(grid)
        mainlayout.appendChild(grid)

        grid = GridLayout(cols = 2, tabular=False, orientation=Orientation.HORIZONTAL)
        grid = fillGrid(grid)
        mainlayout.appendChild(grid)
        mainlayout.appendChild(Label("grid", color="FFFFFF"))

        grid = GridLayout(cols = 2, tabular=True, orientation=Orientation.VERTICAL)
        grid = fillGrid(grid)
        mainlayout.appendChild(grid)

        grid = GridLayout(cols = 2, tabular=True, orientation=Orientation.HORIZONTAL)
        grid = fillGrid(grid)
        mainlayout.appendChild(grid)
        mainlayout.appendChild(Label("table", color="FFFFFF"))



app.App().run(MainDiv(), app_resolution="800x600")
