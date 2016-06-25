#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import libavg
from libavg     import avg, app, player, RectNode

import widgets
from widgets import VLayout, HLayout, Layout, GridLayout, WidgetBase, Orientation
from widgets import ButtonBar, ToggleButtonBar, VLayout, HLayout, Orientation
from widgets import Label
from widgets import StepSlider
from widgets import SnapSwitch,TouchSlider

class MyMainDiv(app.MainDiv):
    def onInit(self):
        snap1 = SnapSwitch( size= (20,230))
        snap2 = SnapSwitch( orientation = Orientation.HORIZONTAL)
        self.appendChild( snap1 )
        self.appendChild( snap2 )

        snap1.pos =  50,50
        snap2.pos = 300,50

        snap1.subscribe(SnapSwitch.STATE_CHANGED, print)
        snap2.subscribe(SnapSwitch.STATE_CHANGED, print)

        slider1 = TouchSlider( pos = (15,320), width= 500, height = 25, parent = self)
        slider2 = TouchSlider( pos = (15,350), width= 500, height = 25, value = 75, range=(0,200),parent = self)
        slider2.subscribe(TouchSlider.VALUE_CANGED, print)
        slider2.subscribe(TouchSlider.RELEASED, print)



    def onExit(self):
        print("thank you for choosing libavg")

    def onFrame(self):
        pass

app.App().run(MyMainDiv())

