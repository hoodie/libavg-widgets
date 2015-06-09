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


import libavg
from libavg      import DivNode, Point2D

class BaseWidget(DivNode):
    def __init__(self, background = None, **kwargs):
        super(BaseWidget, self).__init__(**kwargs)
        self.old_size = Point2D(0,0)

        self.background = background
        if background != None:
            self.__appendChild(background)

        #self.DYNAMIC_SIZE = True


    @property
    def children(self):
        return [self.getChild(i) for i in xrange(self.getNumChildren())]

    def resizeChildren(self, new_size):
        print "resizing children to"
        try:
            ratio = new_size.x/self.old_size.x
        except ZeroDivisionError:
            return False

        # TODO use "self.children"
        for child in self.children:
            child.pos  = child.pos  * ratio
            try:
                child.scale( ratio )
            except AttributeError:
                child.size *= ratio
            print "scaling", child, "by", ratio

        return True

    def resize(self, new_size):
        print "resizing to", new_size
        self.old_size  = self.size
        self.size = new_size
        self.resizeChildren(self.size)
        self.old_size = self.size
        print "called resizeChildren somewhere along the way"

    def scale(self, ratio):
        print "scaling", ratio
        self.resize(self.size * ratio)

    def fillParent(self,size = None):
        # takes size only for SIZE_CHANGED callback
        #self.DYNAMIC_SIZE = False
        self.fillParentV()
        self.fillParentH()

    def fillParentV(self,size = None):
        #self.DYNAMIC_SIZE = False
        self.y = 0
        self.height = self.parent.height
        if self.background != None:
            self.background.size = self.background.size.x, self.parent.height

    def fillParentH(self,size = None):
        #self.DYNAMIC_SIZE = False
        self.x = 0
        self.width = self.parent.width
        if self.background != None:
            self.background.size = self.parent.width, self.background.size.y
