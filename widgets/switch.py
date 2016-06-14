# -*- coding: utf-8 -*-
# UI Element Classes
# Author: Matthias Kalms
# IMLD 2014

from libavg import avg, gesture, geom
from libavg.widget import Orientation

COLORS=[ "b3b3b3", "201f1f", "302f2f" ]

class _SimpleSlider(avg.DivNode):
    def __init__(self,
            initSize=100,
            colors=[],
            orientation=Orientation.HORIZONTAL,
            reverse_node=False, parent=None, **kwargs):
        super(_SimpleSlider, self).__init__(size=(initSize,initSize), **kwargs)

        self.registerInstance(self, parent)

        # initial parameters
        self._initSize 	= initSize
        self._expand    = initSize*2.5
        self._state 	= 0
        self._vertical	= (orientation == Orientation.VERTICAL)
        self.reverse_node = reverse_node
        self.rect_radius  = initSize/2
        self.border_width = initSize/20

        # reverse node direction
        if reverse_node:
            self.rev0 = initSize*3
            self.rev  = -1
        else:
            self.rev0 = 0
            self.rev  = 1

        self._initGraphics(colors)

    ## Init slider graphics.
    # @param self object pointer
    # @param colors list of hex colors for switch [highlight, dark background, light background]
    def _initGraphics(self,colors):
        # set background of switch node
        if self._vertical:
            background = geom.RoundedRect(
                    size=(self._initSize+2*self.border_width, self._expand+2*self.border_width),
                    radius=self.rect_radius,
                    fillopacity=1,
                    fillcolor=colors[1],
                    color="000000",
                    parent= self)
            background.pos = -self.border_width,-self.border_width

        else:
            background = geom.RoundedRect(
                size=(self._expand+2*self.border_width,self._initSize+2*self.border_width),
                radius=self.rect_radius,
                fillopacity=1,
                fillcolor=colors[1],
                color="000000",
                parent=self)
            background.pos = -self.border_width,-self.border_width

        # stretching background node
        self.stretch_rect = geom.RoundedRect(
            size=(self._initSize,self._initSize),
            radius=self.rect_radius,
            fillopacity=1,
            fillcolor=colors[1],
            color=colors[1],
            parent=self)

        # moving node
        self.move_rect = geom.RoundedRect(
            size=(self._initSize,self._initSize),
            radius=self.rect_radius,
            fillopacity=1,
            fillcolor=colors[2],
            color=colors[1],
            strokewidth=3,
            parent=self)
        self.move_rect.pos=(0,0)

    ## Get size of stretch-rect.
    # @param self object pointer
    def getSize(self):
        return self.__divSize

    ## Set size of stretch-rect.
    # @param self object pointer
    # @param size size to be set to
    def setSize(self, size):
        self.move_rect.pos = size - (self._initSize,self._initSize)
        self.stretch_rect.size = size
        if self.reverse_node:
            if self._vertical:
                self.stretch_rect.pos = (0,self.rev0-size.y)
            else:
                self.stretch_rect.pos = (self.rev0-size.x,0)
        else:
            self.stretch_rect.pos = (0,0)
        self.__divSize = size

    def _setState(self, state):
        self._state = state

    __divSize = avg.DivNode.size
    size = property(getSize, setSize)

## Simple 3-state-switchlider.
class SwitchSlider(_SimpleSlider):
    # state of Switch has changed
    STATE_CHANGED = avg.Publisher.genMessageID()

    def __init__(self,
            initSize=100,
            colors=COLORS,
            orientation=Orientation.HORIZONTAL,
            reverse=False,
            friction=-1,
            step = 0,
            parent=None,
            **kwargs):
        super(SwitchSlider, self).__init__(initSize=initSize, colors=colors, orientation=orientation, parent=parent, **kwargs)

        self.publish(self.STATE_CHANGED)

        self.minStretch = 1*initSize
        self.maxStretch = self._expand
        self.steps      = 3
        self.step       = step
        self.stepSize   = (self.maxStretch-self.minStretch)/(self.steps-1)

        # temp values
        self._size = self.size;
        self._pos = self.pos
        self._reverse = reverse;

        # add gesture recognition
        if self._vertical:
            self.setSize(avg.Point2D(initSize,self.minStretch))
            self.recognizer = gesture.DragRecognizer(
                eventNode=self,
                detectedHandler=self.__onDetected,
                moveHandler=self.__onVertMove,
                endHandler=self.__onVertEnd,
                direction=gesture.DragRecognizer.VERTICAL,
                friction=friction)
        else:
            self.setSize(avg.Point2D(self.minStretch, initSize))
            self.recognizer = gesture.DragRecognizer(
                eventNode=self,
                detectedHandler=self.__onDetected,
                moveHandler=self.__onHorizMove,
                endHandler=self.__onHorizEnd,
                direction=gesture.DragRecognizer.HORIZONTAL,
                friction=friction)

        # reverse direction of switch
        if self._reverse:
            self.angle = 3.14
        if self._vertical:
            self.pos = (self._pos.x,self._pos.y + self._expand -self._size.y)
        else:
            self.pos = (self._pos.x + self._expand -self._size.x,self._pos.y)

        # set initial state
        self.setSwitchStep(self.step)

    ## Get switch state.
    # @param self object pointer
    def getSwitchStep(self):
        return self.step

    ## Set switch state.
    # @param self object pointer
    # @param newstate state to be set to
    def setSwitchStep(self, newstate):
        print "trying to update switch"
        self.step = newstate
        self._setState(self.step)
        self._size = avg.Point2D(self._size.x, self.minStretch + newstate*self.stepSize)
        self.setSize(self._size)
        self.notifySubscribers(self.STATE_CHANGED, [self.step])

    ## Update state of switch.
    # @param self object pointer
    def _updateState(self):
        if self._vertical:
            selfValue = self._size.y
        else:
            selfValue = self._size.x
        if (selfValue > (self.maxStretch-0.5*self.stepSize))&(selfValue <= self.maxStretch):
            __step = 2
        if (selfValue > (self.maxStretch-1.5*self.stepSize))&(selfValue <= (self.maxStretch - 0.5*self.stepSize)):
            __step = 1
        if (selfValue > (self.maxStretch-2.5*self.stepSize))&(selfValue <= (self.maxStretch - 1.5*self.stepSize)):
            __step = 0
        if __step != self.step:
            self.step = __step
            self._setState(self.step)
            self.notifySubscribers(self.STATE_CHANGED, [self.step])

    ## Check stretch size to boundaries.
    # @param self object pointer
    # @param newsize size of stretch node
    def _checkBoundaries(self, newsize):
        if self._vertical:
            if newsize.y < self.minStretch:
                newsize.y = self.minStretch;
            if newsize.y > self.maxStretch:
                newsize.y = self.maxStretch;
        else:
            if newsize.x < self.minStretch:
                newsize.x = self.minStretch
            if newsize.x > self.maxStretch:
                newsize.x = self.maxStretch;
        return newsize

    ## On drag gesture recognized.
    # @param self object pointer
    def __onDetected(self):
        self.__dragStartPos = self.pos
        self.__dragStartSize = self.size

    ## On vertical drag move recognized.
    # @param self object pointer
    # @param offset drag offset
    def __onVertMove(self, offset):
        if self._reverse:
            offset.y = - offset.y
        self._size = self._checkBoundaries(self.__dragStartSize + (0,offset.y))
        #self._updateState()
        self.setSize(self._size)
        if self._reverse:
            self.pos = (self._pos.x,self._pos.y + self._expand -self._size.y)

    ## On horizontal drag move recognized.
    # @param self object pointer
    # @param offset drag offset
    def __onHorizMove(self, offset):
        if self._reverse:
            offset.x = - offset.x
        self._size = self._checkBoundaries(self.__dragStartSize + (offset.x, 0))
        #self._updateState()
        self.setSize(self._size)
        if self._reverse:
            self.pos = (self._pos.x + self._expand -self._size.x,self._pos.y)

    ## On vertical drag stop recognized.
    # @param self object pointer
    def __onVertEnd(self):
        self._updateState()
        self._size.y = self.minStretch + self.step*self.stepSize
        self._setState(self.step)
        self.setSize(self._size)
        if self._reverse:
            self.pos = (self._pos.x,self._pos.y + self._expand -self._size.y)

    ## On horizontal drag stop recognized.
    # @param self object pointer
    def __onHorizEnd(self):
        self._updateState()
        self._size.x = self.minStretch + self.step*self.stepSize
        self._setState(self.step)
        self.setSize(self._size)
        if self._reverse:
            self.pos = (self._pos.x + self._expand -self._size.x,self._pos.y)

