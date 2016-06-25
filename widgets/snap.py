# -*- coding: utf-8 -*-
from __future__ import print_function

from libavg import avg, gesture, geom, DivNode
from libavg.widget import Orientation
from widgetbase import WidgetBase

class Slidable(DivNode):
    def __init__(self,
            orientation=None,
            thumb_color = "AAAAAA",
            border_color = "FFFFFF",
            background_color = "444444",
            border_width = 1,
            padding = None,
            parent = None,
            **kwargs):
        super(Slidable, self).__init__(**kwargs)
        self.registerInstance(self, parent)
        self.crop = False

        if orientation == None:
            if min(self.size) == 0:
                self.size = (250,80)
            if self.width > self.height:
                self.orientation = Orientation.HORIZONTAL
            else:
                self.orientation = Orientation.VERTICAL
        else:
            self.orientation  = orientation
            if min(self.size) == 0:
                if self.orientation == Orientation.HORIZONTAL:
                    self.size = (250,80)
                else:
                    self.size = (80,250)

        # values
        self.initSize     = min(self.size)
        self.expand       = max(self.size)
        if padding == None:
            self.padding = self.initSize/10
        else:
            self.padding = float(padding)

        self.rect_radius  = self.initSize-self.padding
        self.friction     = -1
        self.thumb_color       = thumb_color
        self.border_color     = border_color
        self.background_color = background_color
        self.border_width = border_width



        print("orientation: {}".format(self.orientation))
        self.initGraphics()
        self.max_horizontal = self.width-self.thumb.size[0]
        self.max_vertical= self.height-self.thumb.size[1]

    def initGraphics(self):

        self.background = geom.RoundedRect(
            size = self.size,
            radius=self.rect_radius,
            fillopacity=1,
            fillcolor=self.background_color,
            strokewidth=self.border_width,
            color=self.border_color,
            parent=self)

        self.background.pos = 0,0

        # thumb
        self.thumb = geom.RoundedRect(
            size=(self.initSize-self.padding,self.initSize-self.padding),
            radius=self.rect_radius,
            fillopacity=1,
            fillcolor=self.thumb_color,
            color=self.thumb_color,
            strokewidth=0,
            parent=self)




    def initRecognizers(self):
        if self.orientation == Orientation.HORIZONTAL:
            self.recognizer = gesture.DragRecognizer(
                eventNode=self.thumb,
                detectedHandler=self.__onDetected,
                moveHandler=self.onHorizMove,
                endHandler=self.onHorizEnd,
                direction=gesture.DragRecognizer.HORIZONTAL,
                friction=self.friction)
        if self.orientation == Orientation.VERTICAL:
            self.recognizer = gesture.DragRecognizer(
                eventNode=self.thumb,
                detectedHandler=self.__onDetected,
                moveHandler=self.onVertMove,
                endHandler=self.onVertEnd,
                direction=gesture.DragRecognizer.VERTICAL,
                friction=self.friction)

    def __onDetected(self):
        self.__drag_ref = self.thumb.pos

    def displace(self, dist):
        x,y = self.__drag_ref
        if self.orientation == Orientation.HORIZONTAL:
            new_x = x+dist
            new_x = max(new_x, 0)
            new_x = min(new_x, self.max_horizontal)
            newpos = (new_x, y)
        else:
            new_y = y+dist
            new_y = max(new_y, 0)
            new_y = min(new_y, self.max_vertical)
            newpos=(x, new_y)
        self.thumb.pos = newpos


    def maxReached(self): pass
    def minReached(self): pass
    def onVertMove(self, offset):   self.displace(offset[1]);self.onDrag()
    def onHorizMove(self, offset):  self.displace(offset[0]);self.onDrag()


class SnapSwitch(Slidable):
    RELEASED= avg.Publisher.genMessageID()

    STATE_CHANGED = avg.Publisher.genMessageID()

    def __init__(self, **kwargs):
        super(SnapSwitch, self).__init__(**kwargs)
        self.publish(self.STATE_CHANGED)
        self.publish(SnapSwitch.RELEASED)

        # put the thumb in the middle
        if self.orientation == Orientation.HORIZONTAL:
            self.thumb_rest = ((self.expand/2-(self.thumb.size[0])/2),self.padding/2)
        if self.orientation == Orientation.VERTICAL:
            self.thumb_rest = (self.padding/2,(self.expand/2-(self.thumb.size[1])/2))

        self.resetState()
        # setup the thumb
        self.resetThumb()
        self.initRecognizers()
        self.initThumb()

    def initThumb(self):
        # setup the thumb
        if self.orientation == Orientation.HORIZONTAL:
            self.max_dist =  (self.expand/2-(self.thumb.size[0])/2) - self.padding/2
            self.min_dist = -self.max_dist
        if self.orientation == Orientation.VERTICAL:
            self.max_dist =  (self.expand/2-(self.thumb.size[1])/2) - self.padding/2
            self.min_dist = -self.max_dist




    def resetThumb(self):
        # setup the thumb
        if self.orientation == Orientation.HORIZONTAL:
            self.thumb.pos = self.thumb_rest
        if self.orientation == Orientation.VERTICAL:
            self.thumb.pos = self.thumb_rest

    def displace(self, offset):
        x,y = self.thumb_rest
        dist = offset
        dist = min(dist, self.max_dist)
        dist = max(dist, self.min_dist)
        if self.orientation == Orientation.HORIZONTAL:
            newpos = (x+dist, y)
        else:
            newpos=(x, y+dist)
        self.thumb.pos = newpos
        if abs(offset) > self.max_dist:
            if offset < 0: self.minReached()
            if offset > 0: self.maxReached()


    def onHorizEnd(self): self.onDragEnd()
    def onVertEnd(self): self.onDragEnd()

    def onDragEnd(self):
        self.resetThumb()
        self.resetState()
        self.notifySubscribers(self.RELEASED, [0])

    def resetState(self):
        self.min_reached = False
        self.max_reached = False
        self.notifySubscribers(self.STATE_CHANGED, [0])

    def minReached(self):
        if self.min_reached == False:
            self.min_reached = True
            self.max_reached = False
            self.notifySubscribers(self.STATE_CHANGED, [-1])

    def maxReached(self):
        if self.max_reached == False:
            self.max_reached = True
            self.min_reached = False
            self.notifySubscribers(self.STATE_CHANGED, [1])




class TouchSlider(Slidable):

    RELEASED     = avg.Publisher.genMessageID()
    STEPPED      = avg.Publisher.genMessageID()
    VALUE_CANGED = avg.Publisher.genMessageID()

    # FIXME: Ranges from x..y where x>0

    def __init__(self,
            orientation=None,
            border_width = 0,
            range=(0,100),
            value=0,
            padding = 0,
            **kwargs):
        super(TouchSlider, self).__init__(
                orientation=orientation,
                border_width = border_width,
                padding=padding,
                **kwargs)

        self.publish(TouchSlider.RELEASED)
        self.publish(TouchSlider.STEPPED)
        self.publish(TouchSlider.VALUE_CANGED)

        self.__range=range
        self.value = value

        if self.orientation == Orientation.HORIZONTAL:
            thumb_center = self.thumb.size[0]/2
            bar_center  = self.padding/2
            pos = (self.width/(self.__range[1]-self.__range[0]))*value
            self.thumb.pos = (pos, bar_center)
        if self.orientation == Orientation.VERTICAL:
            thumb_center = self.thumb.size[1]/2
            bar_center  = self.padding/2
            pos = ( self.height/( self.__range[1]-self.__range[0]))*value
            self.thumb.pos = ( bar_center, pos)
        self.initRecognizers()

    def resetThumb(self): print("resetting slider")

    def onHorizEnd(self): self.onDragEnd()
    def onVertEnd(self): self.onDragEnd()

    def onDrag(self):
        if self.orientation == Orientation.HORIZONTAL:
            self.value = (self.thumb.pos[0]*(self.__range[1]-self.__range[0]))/self.max_horizontal + self.__range[0]
        else:
            self.value = (self.thumb.pos[1]*(self.__range[1]-self.__range[0]))/self.max_vertical + self.__range[0]
        self.notifySubscribers(TouchSlider.VALUE_CANGED, [self.value]);

    def onDragEnd(self):
        self.notifySubscribers(self.RELEASED, [self.value])

