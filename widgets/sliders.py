# -*- coding: utf-8 -*-
from __future__ import print_function

from libavg import avg, geom, widget as avg_widget, LineNode, DivNode, WordsNode
from skin   import initSkin

def Slider(onPressed = None, onChanged = None, size = 650, thumbPos = 0.5):
    slider          = avg_widget.Slider(skinObj = SKIN)
    slider.size     = avg.Point2D(size, 80)
    slider.thumbPos = thumbPos

    if onChanged:
        slider.subscribe(avg_widget.Slider.THUMB_POS_CHANGED, onChanged)
    if onPressed:
        slider.subscribe(avg_widget.Slider.PRESSED, onPressed)
    return slider


class StepSlider(avg_widget.Slider):
    """A Slider that allows only switching between concrete steps"""

    JUMPED = avg.Publisher.genMessageID()

    def __init__(self,
            orientation=avg_widget.Orientation.HORIZONTAL,
            skinObj= avg_widget.skin.Skin.default,
            steps=[0],
            parent=None,
            **kwargs):
        if orientation == avg_widget.Orientation.HORIZONTAL:
            cfg = skinObj.defaultSliderCfg["horizontal"]
        else:
            cfg = skinObj.defaultSliderCfg["vertical"]

        self.steps = steps
        self.slider_range = kwargs['range']
        self.slider_width = kwargs['width']

        super(StepSlider, self).__init__(orientation, skinObj, **kwargs)
        self.registerInstance(self, parent)
        self.publish(StepSlider.JUMPED)

        self.thumbPos = steps[0]
        self.subscribe(avg_widget.Slider.RELEASED, self._jumpToStep)

    def _initThumb(self, cfg):
        self.drawSteps()
        super(StepSlider, self)._initThumb(cfg)

    def drawSteps(self):
        """
        draws markers at indicating possible steps
        takes place before parent init
        """

        color = "FFFFFF"
        marker_size = 5.,15.
        for step in self.steps:
            marker = DivNode()
            geom.RoundedRect(
                    size=marker_size,
                    radius=2,
                    fillcolor=color,
                    fillopacity=1,
                    opacity=0,
                    parent = marker)

            WordsNode(
                    pos = (marker_size[0]/2,marker_size[1]+3),
                    text=str(step),
                    color=color,
                    fontsize=10,
                    alignment="center",
                    parent = marker)

            marker.pos=(
                    (self.slider_width / self.slider_range[1])*step-marker.width,
                    0)

            self.appendChild(marker)


    def _jumpToStep(self):
        print("jumping to next step")
        min_dist = None
        min_dist_index = 0

        for index, step in enumerate(self.steps):
            dist = abs(step - self.thumbPos)
            if min_dist == None or dist < min_dist:
                min_dist = dist
                min_dist_index = index

        self.setThumbPos(self.steps[min_dist_index])
        # TODO use own Message: JUMPED
        self.notifySubscribers(super(StepSlider, self).THUMB_POS_CHANGED, [self.thumbPos])
        self.notifySubscribers(self.JUMPED, [])
