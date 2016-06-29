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
        snap1 = SnapSwitch( size= (20,120))
        snap2 = SnapSwitch( orientation = Orientation.HORIZONTAL)
        self.appendChild( snap1 )
        self.appendChild( snap2 )

        snap1.pos =  50,20
        snap2.pos = 300,20

        snap1.subscribe(SnapSwitch.STATE_CHANGED, print)
        snap2.subscribe(SnapSwitch.STATE_CHANGED, print)

        TouchSlider( pos = (15,170), width= 500, height = 35, parent = self, padding =-15)
        TouchSlider( pos = (15,230), width= 500, height = 35,
                steps = [0,10,20,40,80,100], parent = self)
        TouchSlider( pos = (15,290), width= 500, height = 35,
                steps = [0,10,20,40,80,100], snap = True, parent = self)
        TouchSlider( pos = (15,350), width= 500, height = 35,
                steps = [0,10,20,40,80,100], snap = True,snap_dist = 5, parent = self)

        slider3 = TouchSlider( pos = (15,400), width= 600, height = 55, value = 75, range=(0,100), steps = [0,10,15,30,50,80,100], parent = self)
        slider3.subscribe(TouchSlider.VALUE_CHANGED, lambda v: print("value changed: {}".format(v)))
        slider3.subscribe(TouchSlider.RELEASED, lambda v:     print("released at:   {}".format(v)))
        slider3.subscribe(TouchSlider.STEPPED, lambda v:      print("stepped to:    {}".format(v)))

        slider4 = TouchSlider(
                pos = (self.width-90,50),
                width= 35, height = 300,
                value = 75,
                range=(0,100),
                steps = [0,25,50,75,100],
                parent = self)


    def onExit(self):
        print("thank you for choosing libavg")

    def onFrame(self):
        pass

app.App().run(MyMainDiv())

