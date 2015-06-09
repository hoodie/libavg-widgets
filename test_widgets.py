#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import libavg
from libavg     import avg, app, player, RectNode

import widgets
from widgets import VLayout, HLayout, Layout, GridLayout, DivNodePlus, Orientation
from widgets import ButtonBar, ToggleButtonBar, VLayout, HLayout, Orientation

class MainDiv(app.MainDiv):

    def onInit(self):
        self.mainlayout = VLayout()
        self.appendChild(self.mainlayout)
        self.buildToolbars()

    def buildToolbars(self):
        toolbarBG = RectNode(fillcolor="424242", opacity=0, fillopacity=1)
        buttonbBG = RectNode(fillcolor="0055FF", opacity=0, fillopacity=0)

        self.toolBar    = HLayout(spacing = 0, background=toolbarBG)

        self.moveBar  = ButtonBar(
            [ widgets.Button("backward_white", tag = "prev"),
              widgets.Button("forward_white", tag = "next") ],
            orientation = libavg.widget.Orientation.HORIZONTAL,
            spacing = 1, background = buttonbBG)

        self.toolBar.appendChild(self.moveBar)
        self.moveBar.subscribe( ButtonBar.CLICKED, self.__handle)
        self.toolBar.pos = 0, self.height - self.toolBar.height
        self.appendChild(self.toolBar)
        self.toolBar.fillParentH()

    def __handle(self, tag):
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
