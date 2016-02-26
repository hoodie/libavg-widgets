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
        mainlayout = GridLayout(cols=3)
        self.appendChild(mainlayout)
        mainlayout.appendChild(demos.demoGrid(cols=3))
        mainlayout.appendChild(demos.nestedLayouts())
        mainlayout.appendChild(demos.scaleLayouts())


app.App().run(MainDiv(), app_resolution="1000x550")
