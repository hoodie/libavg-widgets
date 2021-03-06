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
from widgets import SnapSwitch, TouchSlider

class MainDiv(app.MainDiv):

    def onInit(self):
        mainlayout = VLayout()
        self.appendChild(mainlayout)

        grid = GridLayout(cols= 2, tabular=True, orientation=Orientation.HORIZONTAL, spacing=5)

        slider1 = libavg.widget.Slider(range=(0,100), width=500, thumbPos=60)
        slider2 = libavg.widget.Slider(range=(0,100), width=500)
        slider1.subscribe(slider1.THUMB_POS_CHANGED, slider2.setThumbPos)

        grid.appendChild(Label("Slider", color="FFFFFF")); grid.appendChild(slider1)
        grid.appendChild(Label("linked Slider", color="FFFFFF")); grid.appendChild(slider2)

        grid.appendChild(Label("cafe", color="FFFFFF"))
        grid.appendChild(libavg.widget.ProgressBar(orientation=libavg.widget.Orientation.VERTICAL,
                                                   range=(0,100),
                                                   width=500,
                                                   value=30))

        grid.appendChild(Label("hendrik",color="FFFFFF"))
        grid.appendChild(Label("sollich",color="FFFFFF"))

        grid.appendChild(Label("stepslider",color="FFFFFF"))
        step_slider = StepSlider(
                    range=(0,100),
                    width=500,
                    steps=[0,20,25,50,80, 100])
        step_slider.subscribe(StepSlider.RELEASED, lambda: print("released at ", step_slider.thumbPos))
        step_slider.subscribe(StepSlider.STEPPED, lambda e: print("jumped to ", step_slider.thumbPos, e))
        step_slider.subscribe(StepSlider.THUMB_POS_CHANGED, lambda _pos: print("changed to ", step_slider.thumbPos))
        grid.appendChild( step_slider )


        # SnapSwitch
        switch_slider = SnapSwitch(
                size=(160,80),
                #orientation = Orientation.VERTICAL
                )
        grid.appendChild(Label("switch slider",color="FFFFFF"))
        grid.appendChild( switch_slider )

        # My own Touch Slider
        touch_slider = TouchSlider(
                size=(610,50),
                )
        grid.appendChild(Label("touch slider",color="FFFFFF"))
        grid.appendChild( touch_slider )

        mainlayout.appendChild(grid)

        self.buildToolbars()

    def buildToolbars(self):
        toolbarBG = RectNode(fillcolor="333333", opacity=0, fillopacity=1)

        # main toolbar
        self.toolBar    = HLayout(spacing = 0, background=toolbarBG)

        # forward backward button
        self.naviBar  = ButtonBar(
                [
                    widgets.Button("backward_white", tag = "prev"),
                    widgets.Button("forward_white", tag = "next")
                ],
                orientation = libavg.widget.Orientation.HORIZONTAL,
                spacing = 1,
                background = RectNode(fillcolor="444444", opacity=0, fillopacity=1)
                )

        # some mutually exclusive toggle buttons
        self.toggleBar  = ToggleButtonBar(
                [
                    widgets.ToggleButton("author_white", tag = "figure"),
                    widgets.ToggleButton("attach_white", tag = "clippy")
                ],
                orientation = libavg.widget.Orientation.HORIZONTAL,
                spacing = 1,
                background = RectNode(fillcolor="444444", opacity=0, fillopacity=1)
                )

        # putting it all together
        self.appendChild(self.toolBar)
        self.toolBar.appendChild(self.naviBar)
        self.toolBar.appendChild(self.toggleBar)
        self.toolBar.pos = 0, self.height - self.toolBar.height

        # make everything fit
        self.toolBar.fillParentH()
        self.naviBar.fillParentV()
        self.toggleBar.fillParentV()

        # listen to events
        self.naviBar.subscribe( ButtonBar.CLICKED, self.__handle_navbar)
        self.toggleBar.subscribe( ToggleButtonBar.TOGGLED, self.__handle_toggle)





    def __handle_toggle(self, tag):
        try:
            getattr(self, "handle_"+tag)()
        except AttributeError as details:
            print( "AttributeError: Tag names non existent handler: \"", tag, "\"(" ,details, ")")

    def __handle_navbar(self, tag):
        try:
            getattr(self, "handle_"+tag)()
        except AttributeError as details:
            print( "AttributeError: Tag names non existent handler: \"", tag, "\"(" ,details, ")")


app.App().run(MainDiv(), app_resolution="800x600")
