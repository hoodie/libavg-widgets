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

from libavg import avg, statemachine, player, gesture, geom
from libavg import widget # TODO replace
from widget import Button

        

class SimpleButton(Button):

    def __init__(self,svgId, color="c0c0c0", downcolor= "a0a0a0", opacity= .5,
                tag= None, onPressed= None, **kwargs):
        upcolor= color
        up     = avg.DivNode()
        down   = avg.DivNode()
        up.appendChild(ButtonBackground(upcolor, opacity= opacity))
        up.appendChild(buttonImg(svgId))
        down.appendChild(ButtonBackground(downcolor, opacity= opacity))
        down.appendChild(buttonImg(svgId))
        
        super(Button, self).__init__(up, down, size= (config.ICON_SIZE, config.ICON_SIZE), **kwargs)

        self= widget.Button
        self.tag= tag

        if onPressed:
            self.subscribe(widget.Button.PRESSED, onPressed)
            


def buttonImg(svgId, size= config.ICON_SIZE):
    svg     = avg.SVG(config.SKIN_SVG_PATH)
    bitmap  = svg.renderElement(svgId,size/DPI)
    img     = avg.ImageNode()
    img.setBitmap(bitmap)
    img.pos = avg.Point2D(size/2,size/2) - bitmap.getSize()/2
    return img
    
def ButtonBackground(color, size = config.ICON_SIZE, opacity = 1):
    return geom.RoundedRect(
        (size-2, size-2),
        size/5, (0, 0),
        color       = color, opacity     = opacity,
        fillcolor   = color, fillopacity = opacity)
