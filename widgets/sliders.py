# -*- coding: utf-8 -*-
from __future__ import print_function

from libavg import avg, geom, widget as avg_widget, LineNode, DivNode, WordsNode, gesture
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


# YOU ARE NOT MY REAL SLIDER!!!
class StepSlider(avg_widget.Slider):
    """A Slider that allows only switching between concrete steps"""

    STEPPED = avg.Publisher.genMessageID()

    def __init__(self,
            orientation = avg_widget.Orientation.HORIZONTAL,
            skinObj     = avg_widget.skin.Skin.default,
            steps       = [0],
            parent      = None,
            **kwargs):

        if orientation == avg_widget.Orientation.HORIZONTAL:
            cfg = skinObj.defaultSliderCfg["horizontal"]
        else:
            cfg = skinObj.defaultSliderCfg["vertical"]

        self.steps = steps
        self.slider_orientation = orientation
        self.slider_range = kwargs['range']
        self.slider_width = float(kwargs['width']) if "width" in kwargs else 0
        self.slider_height= kwargs['height'] if "height" in kwargs else 0

        print(skinObj.defaultSliderCfg['vertical'])
        super(StepSlider, self).__init__(orientation, skinObj, **kwargs)
        self.registerInstance(self, parent)
        self.publish(StepSlider.STEPPED)


        self.subscribe(avg_widget.Slider.RELEASED, self._jumpToStep)
        self.setStep(0)

    def _initThumb(self, cfg):
        self.drawSteps()
        super(StepSlider, self)._initThumb(cfg)

    def drawSteps(self):
        """
        draws markers at indicating possible steps
        takes place before parent init
        """

        for index, step in enumerate(self.steps):
            self.addMarker(index,step)

    def addMarker(self,index,step):
        marker = DivNode()
        color = "FFFFFF"

        if self.slider_orientation == avg_widget.Orientation.HORIZONTAL:
            marker_pos=( (self.slider_width / self.slider_range[1])*step-marker.width, 0 )
            marker_size = 5.,15.
            label_pos = (marker_size[0]/2,marker_size[1]+3)
            label_alignment="center"
        else:
            marker_pos=( 0 , (self.slider_height/ self.slider_range[1])*step-marker.height)
            marker_size = 15.,5.
            label_pos = (marker_size[0]+10,marker_size[1]/2)
            label_alignment="left"

        marker.size = (max(marker_size),max(marker_size))
        marker.pos = marker_pos
        marker.tapRecognizer = gesture.TapRecognizer(
                node            = marker,
                #maxTime         = MAX_TAP_TIME,
                maxDist         = 20,
                initialEvent    = None,
                possibleHandler = None,
                failHandler     = None,
                detectedHandler = lambda:  self.setStep(index)
                )


        geom.RoundedRect(
                size=marker_size,
                radius=2,
                fillcolor=color,
                fillopacity=1,
                opacity=0,
                parent = marker)

        WordsNode(
                pos = label_pos,
                text=str(step),
                color=color,
                fontsize=10,
                alignment=label_alignment,
                parent = marker)

        self.appendChild(marker)

    def setStep(self, step_index):
        self.setThumbPos(self.steps[step_index])
        self.notifySubscribers(super(StepSlider, self).THUMB_POS_CHANGED, [self.thumbPos])
        self.notifySubscribers(self.STEPPED, [self.thumbPos])

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
        self.notifySubscribers(super(StepSlider, self).THUMB_POS_CHANGED, [self.thumbPos])
        self.notifySubscribers(self.STEPPED, [self.thumbPos])
