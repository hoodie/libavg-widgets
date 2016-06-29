#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from libavg import app, avg
from widgets import PushNShove

class AppDiv(app.MainDiv, PushNShove):
    def onExit(self): pass
    def onFrame(self): pass

    def addWallNode(self,movenode, callback = lambda: print("no callback set")):
        #self.__animators.append(movenode)
        self.addTransformable( # comes from PushNShove
                movenode,
                tap_callback = lambda(_): callback(),
                #window_decoration = False,
                #zoom_in_callback = lambda(scale): print("scale={}".format(scale)),
                #zoom_in_callback = lambda(scale): scale_spim(scale,movenode),
                resizeable = False
                )


    def onInit(self):
        self.elementoutlinecolor="AA0044"
        self.addWallNode( avg.RectNode( fillopacity=1, size =  (150,150), fillcolor="ffaa00") )
        self.addWallNode( avg.RectNode( fillopacity=1, size =  (150,150), fillcolor="aaff00") )

if __name__ == '__main__':
    # App options (such as app_resolution) can be changed as parameters of App().run()
    app.App().run(AppDiv(), app_resolution='1024x700')


