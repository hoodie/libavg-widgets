from libavg    import avg
from libavg    import widget as avg_widget
import widget_config

def buttonImg(svgId, size= widget_config.ICON_SIZE):
    svg     = avg.SVG(widget_config.SKIN_SVG_PATH)
    bitmap  = svg.renderElement(svgId,size/widget_config.DPI)
    img     = avg.ImageNode()
    img.setBitmap(bitmap)
    img.pos = avg.Point2D(size/2,size/2) - bitmap.getSize()/2
    return img

def ButtonBackground(color, size = widget_config.ICON_SIZE, opacity = 1):
    return avg.RectNode( size = (size,size),
            color = color, opacity = 0, fillcolor = color, fillopacity = 1)
    #return avg.geom.RoundedRect(
    #    (size-2, size-2),
    #    size/5, (0, 0),
    #    color       = color, opacity     = opacity,
    #    fillcolor   = color, fillopacity = opacity)

def Button(svgId, color="c0c0c0", downcolor = "a0a0a0", opacity = .5, tag = None, onPressed = None, size=widget_config.ICON_SIZE, **kwargs):
    upcolor = color
    up      = avg.DivNode()
    down    = avg.DivNode()
    #up.appendChild(ButtonBackground(upcolor, opacity = opacity, size = size))
    up.appendChild(buttonImg(svgId, size = size))
    down.appendChild(ButtonBackground(downcolor, opacity = opacity, size = size))
    down.appendChild(buttonImg(svgId, size = size))

    btn = avg_widget.Button(up, down, size = (size, size), **kwargs)
    btn.tag = tag

    if onPressed:
        btn.subscribe(avg_widget.Button.PRESSED, onPressed)

    return btn

def ToggleButton(svgId, tag=None, size=widget_config.ICON_SIZE, color= "c0c0c0", opacity = .5,**kwargs):
    up      = avg.DivNode()
    down    = avg.DivNode()

    down.appendChild(ButtonBackground(color=color, size=size, opacity=opacity))
    up.appendChild(buttonImg(svgId,size))
    down.appendChild(buttonImg(svgId,size))

    btn = avg_widget.ToggleButton(up, up, down, down, size = (size,size), **kwargs)
    btn.tag = tag
    return btn

