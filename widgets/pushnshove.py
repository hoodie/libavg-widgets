# -*- coding: utf-8 -*-
from __future__ import print_function

import sys, random
from libavg import avg, gesture, DivNode, RectNode, Point2D

# a mixin that holds functionality for basic push and shove wall applications
class PushNShove():

    # Members:
    #
    # self.__floating_windows : [DivNode]
    # self.__connected_windows : [(DivNode,DivNode, PolygonNode)]

    # The Background is currently listening for events -> don't react
    BACKGROUND_SUBSCRIBED = False

    def addTransformable(self,
            node,
            pos               = None,
            transformable     = True,
            resizeable        = False,
            keep_on_screen    = True, # not yet implemented
            window_decoration = True,
            decoration_height = 35,
            tap_callback      = None,
            hold_callback     = None,
            zoom_in_callback  = None,
            zoom_out_callback = None,
            drag_callback     = None,
            drop_callback     = None
            ):

        # put every node in a window
        window = self.__wrapNodeInWindow(
                node,
                window_decoration,
                decoration_height
                )

        # keeping a list of floating windows
        try:
            self.__floating_windows.append(window)
        except AttributeError:
            self.__floating_windows = []
            self.__floating_windows.append(window)


        def tapPossible(): #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            window.previous_size = window.size
            self.deactivateBackground()

        def tapDetected(): #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            if window.tap_callback != None:
                window.tap_callback(window)
            self.deactivateBackground()

        def holdDetected(): #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            window.taprecognizer.abort()
            if window.transformRecognizer != None:
                window.transformRecognizer.abort()
            if window.PS_hold_callback != None:
                window.PS_hold_callback(window)
            else: print("no hold callback")
            self.activateBackground()

        window.transform_resizeable = resizeable
        window.tap_callback         = tap_callback
        window.PS_hold_callback     = hold_callback
        window.PS_drag_callback     = drag_callback
        window.PS_drop_callback     = drop_callback
        window.PS_zoom_in_callback  = zoom_in_callback
        window.PS_zoom_out_callback = zoom_out_callback

        window.PS_old_pos = window.pos

        window.zoom_scale = 1

        window.previous_size = window.size
        window.swiping = False

        # The order of adding tap and transformRecognizers seems to matter
        window.taprecognizer = gesture.TapRecognizer(
                node            = window.decoration,
                possibleHandler = tapPossible,
                detectedHandler = tapDetected)

        window.holdrecognizer = gesture.HoldRecognizer(
                node            = window.decoration,
                #possibleHandler = self.__onPossible,
                detectedHandler = holdDetected,
                #failHandler     = self.__onFail,
                #stopHandler     = self.__onStop
                )

        if transformable:
            self.makeTransformable(window)
        else:
            self.makeNotTransformable(window)

        self.appendChild(window)
        if pos == None:
            self.placeRandomlyOnScreen(window)
        else:
            window.pos = pos

    # adds a connection to self.__connections
    def connectWindows(self, window_a, window_b): # -> bool
        # TODO finish me
        try:
            if window_a in self.__floating_windows() and window_b in self.__floating_windows():
                self.__connected_windows
            return True
        except:
            return False




    def makeNotTransformable(self, window):
        window.transformRecognizer = None

    def makeTransformable(self, window):
        def dragDetected(dist):
            if window.PS_drag_callback != None:
                window.PS_drag_callback(window,dist)

        def dropDetected(dist):
            #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            if window.PS_drop_callback != None:
                window.PS_drop_callback(window, dist)


        def transformDetected():
            #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            if window.parent != None:
                window.parent.reorderChild(window,window.parent.getNumChildren()-1)

        def transformMove(transform):
            #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            if window.transform_resizeable:
                window.size *= transform.scale
            elif transform.scale != 1:
                window.zoom_scale = transform.scale
                transform.scale = 1
            testsize = (window.size * transform.scale)
            #print "testsize ({},{})".format( testsize[0] , testsize[1] )
            transform.rot = 0
            #if MIN_WALLNODE_WIDTH < (window.size * transform.scale).x < MAX_WALLNODE_WIDTH:
            if not window.swiping:
                transform.moveNode(window)
                if window.PS_drag_callback != None:
                    window.PS_drag_callback(window)

            self.keepOnScreen(window) ## keep on screen

        def transformUp(transform):
            #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            self.activateBackground()

        def transformEnd():
            #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            dropDetected((window.pos - window.PS_old_pos).getNorm())
            window.PS_old_pos = window.pos

            if window.zoom_scale < 1:
                zoomOutDetected(window.zoom_scale)

            if window.zoom_scale > 1:
                zoomInDetected(window.zoom_scale)

            window.zoom_scale = 1
            window.pos = (round(window.pos.x), round(window.pos.y))

        def zoomInDetected(scale):
            #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            #print scale
            if window.PS_zoom_in_callback != None:
                window.PS_zoom_in_callback(scale)

        def zoomOutDetected(scale):
            #print "Push-N-Shove " + sys._getframe().f_code.co_name+"()"
            #print scale
            if window.PS_zoom_out_callback != None:
                window.PS_zoom_out_callback(scale)



        window.transformRecognizer = gesture.TransformRecognizer(
                eventNode       = window.decoration,
                coordSysNode    = window,
                detectedHandler = transformDetected,
                moveHandler     = transformMove,
                upHandler       = transformUp,
                endHandler      = transformEnd,
                friction= 0.01
                )

    def focusNode(self, window):
        pass

    def blurNode(self):
        pass

    def blurAllNodes(self):
        pass

    def keepApart(self, window):
        pass #TODO keep nodes from overlappin

    def __wrapNodeInWindow(self, node, decoration,decoration_height): #-> Window: DivNode
        window = DivNode()
        window.crop = True
        border_width = 5
        if decoration:
            window.border= RectNode(
                    strokewidth = 5,
                    pos = (0,0),
                    size =  (node.size[0]+2*border_width, node.size[1]+2*border_width+decoration_height),
                    color="FFFFFF",
                    opacity=1,
                    fillcolor="FFFFFF",
                    fillopacity=1,)

            window.decoration = RectNode(
                    fillopacity=.8,
                    pos = (border_width,border_width),
                    size =  (node.size[0], decoration_height),
                    fillcolor="2299bb")

            window.size = (
                    node.size[0]+2*border_width,
                    node.size[1]+decoration_height+2*border_width)

            window.appendChild(window.border)
            window.appendChild(node)
            window.appendChild(window.decoration)
            node.pos=(0+border_width,decoration_height+border_width)
        else:
            window.decoration = node
            window.size = node.size
            window.appendChild(node)

        return window


    def keepOnScreen(self, window):
        botright = window.pos + window.size
        if window.pos.x < 0:
            window.pos = (0, window.pos.y)

        if window.pos.y < 0:
            window.pos = (window.pos.x, 0)


        if botright.x > self.size.x:
            window.pos = (self.size.x-window.size.x, window.pos.y)

        if botright.y > self.size.y:
            window.pos = (window.pos.x, self.size.y-window.size.y)

    def placeRandomlyOnScreen(self, window):
        pos = ( random.random() * (self.size.x - window.size.x),
                random.random() * (self.size.y - window.size.y))
        window.pos = pos
        self.keepOnScreen(window)

    def activateBackground(self):
        if not self.BACKGROUND_SUBSCRIBED:
            self.subscribe(self.CURSOR_DOWN, self.tapBackground)
            self.BACKGROUND_SUBSCRIBED = True

    def deactivateBackground(self):
        if self.BACKGROUND_SUBSCRIBED:
            self.unsubscribe(self.CURSOR_DOWN, self.tapBackground)
            self.BACKGROUND_SUBSCRIBED = False

    def tapBackground(self, event):
        pass
