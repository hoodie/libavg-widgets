#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import libavg
from libavg     import avg, app, player, RectNode

import widgets
from widgets import VLayout, HLayout, Layout, GridLayout, DivNodePlus, Orientation
from widgets import ButtonBar, ToggleButtonBar, VLayout, HLayout, Orientation
from widgets import Label

class MainDiv(app.MainDiv):

    def onInit(self):
        mainlayout = VLayout()
        self.appendChild(mainlayout)

        grid = GridLayout(cols= 2, tabular=True, orientation=Orientation.HORIZONTAL, spacing=5)
.
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
