#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import libavg
from libavg     import avg, app, player

import widgets
import demos
from widgets import VLayout, HLayout, Layout, GridLayout, DivNodePlus, Orientation

# BaseWidget
#   fillParent
#   fillParentV
#   fillParentH
#   snapToParentTop...

def puts(stuff):
    print stuff

class MainDiv(app.MainDiv):
    def onInit(self):
        mainlayout = GridLayout(cols=2)
        self.appendChild(mainlayout)

        default   = demos.mixedWidthGrid()
        grid_vert = demos.mixedWidthGrid(orientation=Orientation.VERTICAL)
        grid_hori = demos.mixedWidthGrid(orientation=Orientation.HORIZONTAL)

        tab_vert  = demos.mixedWidthTab(orientation=Orientation.VERTICAL)
        tab_hori  = demos.mixedWidthTab(orientation=Orientation.HORIZONTAL)


        mainlayout.appendChild( grid_vert )
        mainlayout.appendChild( grid_hori )

        mainlayout.appendChild( tab_vert )
        mainlayout.appendChild( tab_hori )


app.App().run(MainDiv(), app_resolution="1000x700")
