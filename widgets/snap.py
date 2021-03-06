# -*- coding: utf-8 -*-
from __future__ import print_function

from libavg import avg, gesture, DivNode, WordsNode
from libavg.geom   import RoundedRect
from libavg.widget import Orientation

class Slidable(DivNode):
    TAPPED = avg.Publisher.genMessageID()

    def __init__(self,
                 orientation=None,
                 thumb_color = "777777",
                 font_color = "FFFFFF",
                 border_color = "FFFFFF",
                 background_color = "333333",
                 thumb_label=False,
                 border_width = 1,
                 padding = None,
                 parent = None,
                 **kwargs):
        super(Slidable, self).__init__(**kwargs)
        self.registerInstance(self, parent)
        self.crop = False
        self.publish(Slidable.TAPPED)

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
                if self.orientation == Orientation.VERTICAL:
                    self.size = (80,250)

        # values
        self.initSize     = min(self.size)
        self.expand       = max(self.size)
        if padding == None:
            self.padding = self.initSize/10
        else:
            self.padding = float(padding)

        self.rect_radius      = self.initSize-self.padding
        self.friction         = -1
        self.thumb_color      = thumb_color
        self.font_color       = font_color
        self.border_color     = border_color
        self.background_color = background_color
        self.border_width     = border_width
        self.thumb_label_on   = thumb_label



        #print("TouchSlider: orientation: {}".format(self.orientation))
        self.initGraphics()
        self.max_horizontal = self.width-self.thumb.size[0]
        self.max_vertical= self.height-self.thumb.size[1]

    def initGraphics(self):

        self.background = RoundedRect(
            size = self.size,
            radius=self.rect_radius,
            opacity=0,
            fillopacity=1,
            fillcolor=self.background_color,
            strokewidth=self.border_width,
            color=self.border_color,
            parent=self)

        def handle_cursor(event):
            tapped = self.background.getRelPos(event.contact.events[0].pos)[0]/self.background.size[0]
            self.notifySubscribers(Slidable.TAPPED, [tapped])

        self.background.subscribe( self.background.CURSOR_DOWN, handle_cursor )
        self.background.pos = 0,0

        thumb_size=(self.initSize-self.padding,self.initSize-self.padding)
        # thumb
        self.thumb = DivNode(pos         = (0,0),
                             size        = thumb_size,
                             parent = self)

        RoundedRect(pos         = (0,0),
                    size        = thumb_size,
                    radius      = self.rect_radius,
                    fillopacity = 1,
                    fillcolor   = self.thumb_color,
                    color       = self.thumb_color,
                    strokewidth = 0,
                    parent      = self.thumb)

        fontsize = 12
        if self.thumb_label_on:
            self.thumb_label = WordsNode(
                    pos = (thumb_size[0]/2, thumb_size[1]/2-fontsize/2),
                    color=self.font_color,
                    fontsize=fontsize,
                    alignment="center",
                    parent = self.thumb)
        else: self.thumb_label = None





    def initRecognizers(self):
        if self.orientation == Orientation.HORIZONTAL:
            self.dragRecognizer = gesture.DragRecognizer(
                eventNode=self.thumb,
                detectedHandler=self.__onDetected,
                moveHandler=self.onHorizMove,
                endHandler=self.onHorizEnd,
                direction=gesture.DragRecognizer.HORIZONTAL,
                friction=self.friction)
        if self.orientation == Orientation.VERTICAL:
            self.dragRecognizer = gesture.DragRecognizer(
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

    def onDrag(self): pass
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
    VALUE_CHANGED = avg.Publisher.genMessageID()

    # FIXME: Ranges from x..y where x>0

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        if self.thumb_label: self.thumb_label.text = str(int(v))
        self.__value = v

    def __init__(self,
                 orientation=None,
                 border_width = 0,
                 range=(0,100),
                 value=0,
                 snap= False,
                 snap_dist = 1000000,
                 steps = [],
                 padding = 0,
                 **kwargs):
        super(TouchSlider, self).__init__(
                orientation=orientation,
                border_width = border_width,
                padding=padding,
                **kwargs)

        self.publish(TouchSlider.RELEASED)
        self.publish(TouchSlider.STEPPED)
        self.publish(TouchSlider.VALUE_CHANGED)

        self.__markers = []
        self.__range=range

        self.steps = steps
        self.snap_dist = snap_dist
        self.__value = value

        self.setValue(value)

        self.initRecognizers()
        if len(steps) > 0:
            self.addMarkers()
        if snap:
            #print("TouchSlider: enabling snap")
            self.subscribe(TouchSlider.RELEASED, self.jumpToStep)

        self.subscribe(Slidable.TAPPED, lambda val: self.setValue(val*self.__range[1], jump_to_step=True))

    def setValue(self,value, jump_to_step = False, notify=True):
        self.value = value
        self.thumb.pos = self.placeOnBar(self.thumb,value)
        if jump_to_step: self.jumpToStep(value)
        if notify: self.notifySubscribers(TouchSlider.VALUE_CHANGED, [self.value])


    def resetThumb(self): pass #print("TouchSlider: resetting slider")

    def onHorizEnd(self): self.onDragEnd()
    def onVertEnd(self): self.onDragEnd()

    def onDrag(self):
        if self.orientation == Orientation.HORIZONTAL:
            self.value = (self.thumb.pos[0]*(self.__range[1]-self.__range[0]))/self.max_horizontal + self.__range[0]
        if self.orientation == Orientation.VERTICAL:
            self.value = (self.thumb.pos[1]*(self.__range[1]-self.__range[0]))/self.max_vertical + self.__range[0]
        self.notifySubscribers(TouchSlider.VALUE_CHANGED, [self.value]);

    def onDragEnd(self):
        self.notifySubscribers(self.RELEASED, [self.value])

    def removeMarkers(self):
        self.steps = []
        for marker in self.__markers:
            self.removeChild(marker)
        self.__markers = []

    def addMarkers(self):
        """
        draws markers at indicating possible steps
        takes place before parent init
        """

        for step in self.steps:
            self.addMarkerByValue(step)

    #TODO def addMarkerByIndex(self,index): both by step and by index
    def addMarkerByIndex(self,index):
        addMarkerByValue(self.steps[index])

    def addMarkerByValue(self,value):
        if self.orientation == Orientation.HORIZONTAL:
            marker_size = 5,self.height
        if self.orientation == Orientation.VERTICAL:
            marker_size = self.width,5

        marker = self.drawMarker(marker_size, value, self.orientation)
        marker.tapRecognizer = gesture.TapRecognizer(
                node            = marker,
                maxDist         = 30,
                initialEvent    = None,
                possibleHandler = None,
                failHandler     = None,
                detectedHandler = lambda:  self.setValue(value))


        marker.pos = self.placeOnBar(marker,value)
        self.__markers.append(marker)
        self.appendChild(marker)


    # sets the position of an Node
    def placeOnBar(self, node, step, size=None):
        if size == None: size = node.size

        if self.orientation == Orientation.HORIZONTAL:
            thumb = self.thumb.size[0]
            marker_pos=(
                    ((self.width-thumb)/ self.__range[1])
                    *step-size[0]/2
                    + thumb/2,
                    0 )

        if self.orientation == Orientation.VERTICAL:
            thumb = self.thumb.size[1]
            marker_pos=( 0 ,
                    ((self.height-thumb)/ self.__range[1])
                    *step-size[1]/2
                    + thumb/2)

        return marker_pos



    #  overwrite this
    def drawMarker(self, size, value, orientation): # -> DivNode
        color = "FFFFFF"
        sensitive = True
        marker = DivNode(sensitive=sensitive)
        marker.size = size #max(size), max(size)

        if self.orientation == Orientation.HORIZONTAL:
            label_pos = (marker.size[0]/2,marker.size[1]+3)
            label_alignment="center"

        if self.orientation == Orientation.VERTICAL:
            label_pos = (marker.size[0]+10,marker.size[1]/2)
            label_alignment="left"

        bar = RoundedRect(
                size=size,
                radius=2,
                fillcolor=color,
                fillopacity=1,
                opacity=0,
                parent = marker)

        WordsNode(
                pos = label_pos,
                text=str(value),
                color=color,
                fontsize=10,
                alignment=label_alignment,
                parent = marker)

        return marker

    def jumpToStep(self, value):
        min_dist = None
        min_dist_index = 0

        for index, step in enumerate(self.steps):
            dist = abs(step - self.value)
            if min_dist == None or dist < min_dist:
                min_dist = dist
                min_dist_index = index

        #print("TouchSlider: jump to step from", value, "to", min_dist_index)
        #print("             min_dist = {} snap_dist = {}".format(min_dist,self.snap_dist))
        if min_dist < self.snap_dist and min_dist_index < len(self.steps):
            self.setValue(self.steps[min_dist_index])
            #print("             actually stepping")
        else:
            #print("             not stepping", self.steps)
            pass
        self.notifySubscribers(self.STEPPED, [self.value])
