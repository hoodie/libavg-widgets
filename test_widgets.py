#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

        grid.appendChild(Label("foo"    ,color="0000FF"))
        grid.appendChild(Label("bar"    ,color="0000FF"))
        grid.appendChild(Label("cafe"   ,color="FF00FF"))
        grid.appendChild(Label("babe"   ,color="FF00FF"))
        grid.appendChild(Label("hendrik",color="FF0000"))
        grid.appendChild(Label("sollich",color="FF0000"))

        mainlayout.appendChild(grid)

        self.buildToolbars()

    def buildToolbars(self):
        toolbarBG = RectNode(fillcolor="ff0000", opacity=0, fillopacity=1)
        buttonbBG = lambda: RectNode(fillcolor="0000FF", opacity=0, fillopacity=1)

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
                background = RectNode(fillcolor="0000FF", opacity=0, fillopacity=1)
                )

        # some mutually exclusive toggle buttons
        self.toggleBar  = ToggleButtonBar(
                [
                    widgets.ToggleButton("author_white", tag = "figure"),
                    widgets.ToggleButton("attach_white", tag = "clippy")
                ],
                orientation = libavg.widget.Orientation.HORIZONTAL,
                spacing = 1,
                background = RectNode(fillcolor="0000FF", opacity=0, fillopacity=1)
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
            print "AttributeError: Tag names non existent handler: \"", tag, "\"(" ,details, ")"

    def __handle_navbar(self, tag):
        try:
            getattr(self, "handle_"+tag)()
        except AttributeError as details:
            print "AttributeError: Tag names non existent handler: \"", tag, "\"(" ,details, ")"

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


app.App().run(MainDiv(), app_resolution="800x600")
