# -*- coding: utf-8 -*-
# libavg - Media Playback Engine.
# Copyright (C) 2003-2014 Ulrich von Zadow
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Current versions can be found at www.libavg.de
#
# Original author of this file is Hendrik Sollich


import math
import libavg
from widget import BaseWidget
from libavg import DivNode

#TODO Layout: border
#TODO Layout: don't keep extra list of objects but give them attributes (child.isMinion)
class Orientation:
    VERTICAL     = 0
    HORIZONTAL   = 1

class GridLayout(BaseWidget):
    RENDERED = libavg.Publisher.genMessageID()

    def __init__(self,
            cols = -1,
            rows = -1,
            spacing = 5,
            orientation = Orientation.HORIZONTAL,
            tabular = False,
            background = None,
            onRendered = None,
            **kwargs):
        super(GridLayout, self).__init__(**kwargs)

        self.ORIENTATION = orientation
        self.TABULAR = tabular

        if rows < 0 and cols < 0:
            raise(RuntimeError("GridLayout: Either rows or cols must bit set"))

        self.cols = cols
        self.rows = rows

        self.publish(self.RENDERED)
        self.spacing = float(spacing)

        self.background = background
        if background != None:
            self.__appendChild(background)

        self.__layoutedChildren = [] # not children because children include the background as well

        if onRendered != None:
            self.subscribe(self.RENDERED, onRendered)

    def __appendChild(self, child):
        return super(GridLayout, self).appendChild(child)

    def appendChildren(self, children):
        for child in children:
            self.appendChild(child)

    def removeChild(self, child):
        child.unlink()
        self.__layoutedChildren.remove(child)
        self.render()

    def appendChild(self, child):
        self.__layoutedChildren.append(child)
        self.__appendChild(child)
        self.render()

    def render(self):
        if self.TABULAR == True:
            self.render_tabular()
        else:
            if self.ORIENTATION == Orientation.HORIZONTAL:
                self.render_horizontal()
            elif self.ORIENTATION == Orientation.VERTICAL:
                self.render_vertical()

    def render_horizontal(self):
        pos = libavg.Point2D(0, 0)
        col_width = row_height = 0
        row_heights = {}

        if self.cols > 0:
            rows = int(math.ceil( float(len(self.__layoutedChildren)) / self.cols ))
            cols = self.cols
        elif self.rows > 0:
            cols = int(math.ceil( float(len(self.__layoutedChildren)) / self.rows ))
            rows = self.rows


        for i, child in enumerate(m for m in self.__layoutedChildren if m.active):
            if i%cols == 0:
                pos.x  = self.spacing/2
                pos.y += self.spacing/2 + row_height
                col_width = row_height = self.spacing/2

            child.pos = (pos.x, pos.y)
            pos.x += child.size.x + self.spacing/2
            col_width  += child.size.x + self.spacing/2
            row_height = max(row_height, child.size.y)
            row_heights[i/cols] = row_height + self.spacing/2

            #TODO too small, not right
            self.width  = max(self.width, col_width)
        self.height = sum(row_heights.values()) + self.spacing/2
        self.old_size = self.size # used by scale
        if self.background != None:
            self.background.size = self.size

        self.notifySubscribers(self.RENDERED, [self])

    def render_vertical(self):
        pos = libavg.Point2D(0, 0)
        row_height = col_width = 0
        col_widths = {}

        if self.rows > 0:
            cols = int(math.ceil( float(len(self.__layoutedChildren)) / self.rows ))
            rows = self.rows
        elif self.cols > 0:
            rows = int(math.ceil( float(len(self.__layoutedChildren)) / self.cols ))
            cols = self.cols


        for i, child in enumerate(m for m in self.__layoutedChildren if m.active):
            if i%rows == 0:
                pos.y  = self.spacing/2
                pos.x += self.spacing/2 + col_width
                row_height = col_width = self.spacing/2

            child.pos = (pos.x, pos.y)
            pos.y += child.size.y + self.spacing/2
            row_height  += child.size.y + self.spacing/2
            col_width = max(col_width, child.size.x)
            col_widths[i/rows] = col_width + self.spacing/2

            #TODO too small, not right
            self.height  = max(self.height, row_height)
        self.width = sum(col_widths.values()) + self.spacing/2
        self.old_size = self.size # used bx scale
        if self.background != None:
            self.background.size = self.size

        self.notifySubscribers(self.RENDERED, [self])

    def render_tabular(self): # quasi horizontal
        pos = libavg.Point2D(0, 0)
        row_height = col_width = 0

        col_widths  = {}
        row_heights = {}

        if self.rows > 0:
            cols = int(math.ceil( float(len(self.__layoutedChildren)) / self.rows ))
            rows = self.rows
        elif self.cols > 0:
            rows = int(math.ceil( float(len(self.__layoutedChildren)) / self.cols ))
            cols = self.cols

        col_index = row_index = -1

        # layouting run
        for i, child in enumerate(m for m in self.__layoutedChildren if m.active):

            if self.ORIENTATION == Orientation.VERTICAL:
                col_index=i/cols
                row_index=i%rows

            elif self.ORIENTATION == Orientation.HORIZONTAL:
                col_index=i%cols
                row_index=i/rows


            width  = max(col_widths .get(col_index, -1),  child.width + self.spacing/2)
            height = max(row_heights.get(row_index, -1), child.height + self.spacing/2)

            col_widths[col_index]  = width
            row_heights[row_index] = height

            print col_index, row_index, width, height

        col_widths[-1] = 0 # hack for the [-1] case
        row_heights[-1] = 0 # hack for the [-1] case

        # layouting run
        for i, child in enumerate(m for m in self.__layoutedChildren if m.active):

            if self.ORIENTATION == Orientation.VERTICAL:
                col_index=i/cols
                row_index=i%rows

            elif self.ORIENTATION == Orientation.HORIZONTAL:
                col_index=i%cols
                row_index=i/rows

            child.pos = (
                    sum(col_widths.values()[0:col_index]) + self.spacing/2,
                    sum(row_heights.values()[0:row_index])+ self.spacing/2
                        )

        self.height = sum(row_heights.values()) + self.spacing/2
        self.width  = sum(col_widths.values())  + self.spacing/2
        self.old_size = self.size # used by scale
        if self.background != None:
            self.background.size = self.size

        self.notifySubscribers(self.RENDERED, [self])


    # for hlayout
    def center_rows(self):
        for child in self.children:
            if child is not self.background:
                child.pos = (child.pos.x, self.height/2-child.height/2)

    # for hlayout
    def center_columns(self):
        for child in self.children:
            if child is not self.background:
                child.pos = (self.width/2-child.width/2, child.pos.y)

class HLayout(GridLayout):
    def __init__(self, **kwargs):
        super(HLayout, self).__init__(rows = 1,**kwargs)

class VLayout(GridLayout):
    def __init__(self, **kwargs):
        super(VLayout, self).__init__(cols = 1, **kwargs)

## strictly legacy support
class Layout(GridLayout):
    def __init__(self, orientation=Orientation, spacing = 5, background = None, onRendered = None, **kwargs):
        rows = cols = -1
        if orientation == Orientation.VERTICAL:
            cols = 1
        elif orientation == Orientation.HORIZONTAL:
            rows = 1
        super(Layout,self).__init__(cols=cols,rows=rows,spacing=spacing,background=background,onRendered=onRendered,**kwargs)

class TableLayout(GridLayout):
    def __init__(self,
            orientation=Orientation,
            spacing = 5,
            background = None,
            onRendered = None,
            tabular = True,
            **kwargs):
        rows = cols = -1
        if orientation == Orientation.VERTICAL:
            cols = 1
        elif orientation == Orientation.HORIZONTAL:
            rows = 1
        super(Layout,self).__init__(cols=cols,rows=rows,spacing=spacing,background=background,onRendered=onRendered,**kwargs)
