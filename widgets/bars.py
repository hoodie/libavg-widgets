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

from layout import Layout

class ButtonBar(Layout):
    CLICKED = libavg.Publisher.genMessageID()
    PRESSED = libavg.Publisher.genMessageID()

    def __init__(self, buttons, spacing = 4, **kwargs):
        super(ButtonBar, self).__init__(**kwargs)

        self.publish(self.CLICKED)
        self.publish(self.PRESSED)
        self.buttons = buttons
        self.appendChildren(self.buttons)

        for button in buttons:
            button.subscribe(button.CLICKED, lambda button=button: self.__onClicked(button.tag))
            button.subscribe(button.PRESSED, lambda button=button: self.__onPressed(button.tag))

    def __onClicked(self, tag):
        self.notifySubscribers(self.CLICKED, [tag])

    def __onPressed(self, tag):
        self.notifySubscribers(self.PRESSED, [tag])

class ToggleButtonBar(Layout):
    TOGGLED = libavg.Publisher.genMessageID()

    def __init__(self, buttons, onToggled = None, **kwargs):
        super(ToggleButtonBar, self).__init__(**kwargs)

        self.publish(self.TOGGLED)
        if onToggled:
            self.subscribe(self.TOGGLED, onToggled)

        self.buttons = buttons
        self.appendChildren(self.buttons)

        for button in buttons:
            button.subscribe(button.TOGGLED,
                             lambda checked,
                             button=button: self.__onToggled(button))

    #def index(self, tag):
    #    return [btn.tag == tag for btn in self.buttons].index(True)

    def toggle_silently(self, index, checked = True):
        button = self.buttons[index]
        for btn in self.buttons:
            btn.enabled = True
            btn.checked = False
        if checked:
            button.enabled = False
            button.checked = True
        else:
            button.enabled = True
            button.checked = False

    def toggle(self, index, checked = True):
        button = self.buttons[index]
        self.toggle_silently(index, checked = True)
        self.__onToggled(button)

    def untoggle(self):
        for btn in self.buttons:
            btn.enabled = True
            btn.checked = False

    def __onToggled(self, button):
        if button.checked:
            button.enabled = False
        for otherButton in self.buttons:
            if otherButton != button:
                otherButton.checked = False
                otherButton.enabled = True
        self.notifySubscribers(self.TOGGLED, [button.tag])
