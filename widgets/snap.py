# -*- coding: utf-8 -*-
from __future__ import print_function

from libavg import avg, gesture, geom
from libavg.widget import Orientation
from widgetbase import WidgetBase

class SnapSwitch(WidgetBase):

    STATE_CHANGED = avg.Publisher.genMessageID()

    def __init__(self,
            orientation=Orientation.HORIZONTAL,
            knob_color = "AAAAAA",
            border_color = "FFFFFF",
            background_color = "444444",
            initSize=100,
            **kwargs):
        super(SnapSwitch, self).__init__(propagate_size_changed = False,**kwargs)
        self.publish(self.STATE_CHANGED)

        # values
        self.__orientation  = orientation
        self.__initSize     = initSize
        self.__expand       = initSize*2.5
        self.__border_width = initSize/20
        self.__rect_radius  = initSize/2
        self.__friction     = -1
        self.__knob_color       = knob_color
        self.__border_color     = border_color
        self.__background_color = background_color

        self.__initGraphics()
        self.__resetState()



    def __initGraphics(self):
        # set background of switch node
        bw = self.__border_width
        if self.__orientation == Orientation.VERTICAL:
            self.__background = geom.RoundedRect(
                    size=(self.__initSize+2*self.__border_width, self.__expand+2*self.__border_width),
                    radius=self.__rect_radius,
                    fillopacity=1,
                    fillcolor=self.__background_color,
                    color=self.__border_color,
                    parent= self)

        else:
            self.__background = geom.RoundedRect(
                size=(self.__expand+2*self.__border_width,self.__initSize+2*self.__border_width),
                radius=self.__rect_radius,
                fillopacity=1,
                fillcolor=self.__background_color,
                color=self.__border_color,
                parent=self)

        bgsize = self.__background.size
        self.__background.pos = bw,bw
        self.size = bgsize[0]+2*bw, bgsize[1]+2*bw

        # knob
        self.__knob = geom.RoundedRect(
            size=(self.__initSize,self.__initSize),
            radius=self.__rect_radius,
            fillopacity=1,
            fillcolor=self.__knob_color,
            color=self.__knob_color,
            strokewidth=0,
            parent=self)
        self.__knob.pos=(2*bw,2*bw)

        # setup the knob
        self.__centerKnob()

        if self.__orientation == Orientation.HORIZONTAL:
            self.recognizer = gesture.DragRecognizer(
                eventNode=self.__knob,
                detectedHandler=self.__onDetected,
                moveHandler=self.__onHorizMove,
                endHandler=self.__onHorizEnd,
                direction=gesture.DragRecognizer.HORIZONTAL,
                friction=self.__friction)

        if self.__orientation == Orientation.VERTICAL:
            self.recognizer = gesture.DragRecognizer(
                eventNode=self.__knob,
                detectedHandler=self.__onDetected,
                moveHandler=self.__onVertMove,
                endHandler=self.__onVertEnd,
                direction=gesture.DragRecognizer.VERTICAL,
                friction=self.__friction)

    def __centerKnob(self):
        # setup the knob
        bw = self.__border_width
        if self.__orientation == Orientation.HORIZONTAL:
            self.__max_dist =  (self.__expand/2-(self.__knob.size[0]-bw)/2)
            self.__min_dist = -(self.__expand/2-(self.__knob.size[0]+bw)/2)
            self.__knob.pos = (self.__max_dist+bw,2*bw)
            self.__knob_pos = (self.__max_dist+bw,2*bw)
        if self.__orientation == Orientation.VERTICAL:
            self.__max_dist =  (self.__expand/2-(self.__knob.size[1]-bw)/2)
            self.__min_dist = -(self.__expand/2-(self.__knob.size[1]+bw)/2)
            self.__knob.pos = (2*bw,self.__max_dist+bw)
            self.__knob_pos = (2*bw,self.__max_dist+bw)


    def __onDetected(self):
        #print("moving a knob", self.__knob)
        pass

    def __onVertMove(self, offset):
        #print("move vert", self.__knob)
        x,y = self.__knob_pos
        dist = offset[1]
        dist = min(dist, self.__max_dist)
        dist = max(dist, self.__min_dist)
        newpos=(x, y+dist)
        self.__knob.pos = newpos
        if abs(offset[1]) > self.__max_dist:
            if offset[1] < 0: self.__minReached()
            if offset[1] > 0: self.__maxReached()

    def __onHorizMove(self, offset):
        x,y = self.__knob_pos
        dist = offset[0]
        dist = min(dist, self.__max_dist)
        dist = max(dist, self.__min_dist)
        newpos = (x+dist, y)
        if abs(offset[0]) > self.__max_dist:
            if offset[0] < 0: self.__minReached()
            if offset[0] > 0: self.__maxReached()

        self.__knob.pos = newpos

    def __onDragEnd(self):
        self.__centerKnob()
        self.__resetState()

    def __onHorizEnd(self): self.__onDragEnd()
    def __onVertEnd(self): self.__onDragEnd()

    def __resetState(self):
        self.__min_reached = False
        self.__max_reached = False
        self.notifySubscribers(self.STATE_CHANGED, [0])

    def __minReached(self):
        if self.__min_reached == False:
            self.__min_reached = True
            self.__max_reached = False
            self.notifySubscribers(self.STATE_CHANGED, [-1])

    def __maxReached(self):
        if self.__max_reached == False:
            self.__max_reached = True
            self.__min_reached = False
            self.notifySubscribers(self.STATE_CHANGED, [1])

