# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from libavg import avg, geom, widget as avg_widget

def initSkin():
    pwdPath = os.path.dirname(os.path.realpath(__file__))
    mediaPath = os.path.join(pwdPath, "skin")
    return avg_widget.Skin("CustomSkin.xml", mediaPath)

