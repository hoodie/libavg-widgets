from libavg    import avg, widget

class RoomWidget(avg.DivNode):

    BOX_COLOR = "FFFF66"
    TAB_COLOR0= "AA3333"
    TAB_COLOR1= "FF6666"
    STROKEWIDTH = 1

    def __init__(self, height=200, width=200, label="unnamed sensor", parent=None, *args, **kwargs):
        super(RoomWidget, self).__init__(*args, **kwargs)
        #tablet = self.projectVerts(self.getTablet())
        self.height = height
        self.width  = width
        print "WIM: size:", self.size

        self.__background = avg.RectNode( size = (self.height, self.width),
                                          fillopacity=1,
                                          fillcolor="222222",
                                          parent=self)

        box 	= self.box 	  = self.getBox()

        tablet 	= self.tablet = self.getTablet()
        self.initBox()
        self.updateBox(box)
        self.initTablet()
        self.updateTablet(tablet)


    def initBox(self):
        self.boxLines = [
            avg.LineNode(strokewidth=self.STROKEWIDTH, color=self.BOX_COLOR, parent=self) for _ in range(12)]

    def initTablet(self):
        self.tabletLines = [
            avg.LineNode(strokewidth=self.STROKEWIDTH,   color=self.TAB_COLOR0, parent=self), # top
            avg.LineNode(strokewidth=self.STROKEWIDTH+1, color=self.TAB_COLOR1, parent=self), # right
            avg.LineNode(strokewidth=self.STROKEWIDTH+2, color=self.TAB_COLOR1, parent=self), # bottom
            avg.LineNode(strokewidth=self.STROKEWIDTH,   color=self.TAB_COLOR0, parent=self), # left
            ]

    def updateTablet(self, verts):
        verts = self.projectVerts(verts)
        self.tabletLines[0].pos1 = verts[0]
        self.tabletLines[0].pos2 = verts[1]
        self.tabletLines[1].pos1 = verts[1]
        self.tabletLines[1].pos2 = verts[2]
        self.tabletLines[2].pos1 = verts[2]
        self.tabletLines[2].pos2 = verts[3]
        self.tabletLines[3].pos1 = verts[3]
        self.tabletLines[3].pos2 = verts[0]

    def updateBox(self,verts):
        verts = self.projectVerts(verts)
        self.boxLines[0].pos1 = verts[0]
        self.boxLines[0].pos2 = verts[1]
        self.boxLines[1].pos1 = verts[1]
        self.boxLines[1].pos2 = verts[3]
        self.boxLines[2].pos1 = verts[0]
        self.boxLines[2].pos2 = verts[2]
        self.boxLines[3].pos1 = verts[2]
        self.boxLines[3].pos2 = verts[3]
        self.boxLines[4].pos1 = verts[4]
        self.boxLines[4].pos2 = verts[5]
        self.boxLines[5].pos1 = verts[5]
        self.boxLines[5].pos2 = verts[7]
        self.boxLines[6].pos1 = verts[4]
        self.boxLines[6].pos2 = verts[6]
        self.boxLines[7].pos1 = verts[6]
        self.boxLines[7].pos2 = verts[7]
        self.boxLines[8].pos1 = verts[0]
        self.boxLines[8].pos2 = verts[4]
        self.boxLines[9].pos1 = verts[1]
        self.boxLines[9].pos2 = verts[5]
        self.boxLines[10].pos1 = verts[2]
        self.boxLines[10].pos2 = verts[6]
        self.boxLines[11].pos1 = verts[3]
        self.boxLines[11].pos2 = verts[7]

    def getTablet(self, w = 16, h = 9): #-> [(float,float,float);6]
        w = (w * self.width) / 500
        h = (h * self.width) / 500

        return [ (-w/2, -h/2, 0),
                 ( w/2, -h/2, 0),
                 ( w/2,  h/2, 0),
                 (-w/2,  h/2, 0) ]

    def getBox(self): #-> [(float,float,float);6]
        s = self.width/50
        box = [
                (-s,-s,-s),
                ( s,-s,-s),
                (-s, s,-s),
                ( s, s,-s),

                (-s,-s, s),
                ( s,-s, s),
                (-s, s, s),
                ( s, s, s),
                ]
        return box

    def projectVerts(self,verts): #-> [(float,float);6]
        offset = self.width / 2 ## nach oben links
        depth = .4
        new_verts = []
        dist = 150
        for x,y,z in verts:

            x *= 15
            y *= 15
            z *= 15

            z = z * depth
            new_verts.append((x+z+offset, y-z+offset))

            #z1 = z * .8
            #z2 = (z+dist)/150.0
            #new_verts.append(( (x+z1)/z2 +offset, (y+z1)/z2 +offset))

            #z = (z+dist)/170.0
            #new_verts.append( (x/z+offset,   y/z+offset))
        return new_verts
