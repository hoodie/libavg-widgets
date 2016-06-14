from libavg import Point2D, DivNode, WordsNode


class WidgetBase(DivNode):

    def __init__(self,
                 parent = None,
                 background = None,
                 propagate_size_changed = True,
                 *args, **kwargs):

        super(WidgetBase, self).__init__(crop = True, *args, **kwargs)

        self.registerInstance(self, parent)
        self.old_size = self.size
        self.background = background
        if propagate_size_changed:
            self.subscribe(self.SIZE_CHANGED, self.resizeChildren)

    # children need to be handled nicer, don't you agree?
    @property
    def children(self):
        return [self.getChild(i) for i in xrange(self.getNumChildren())]

    def children_each(self, block):
        for child in self.children:
            block.__call__(child)

    def resizeChildren(self, new_size):
        if self.old_size.x == 0:
            self.old_size = self.size

        try:
            ratio = new_size.x/self.old_size.x
        except ZeroDivisionError:
            return False

        if ratio == 1:
            return False

        for child in self.children:
            #print "     WidgetBase::resizeChildren() resizing by {0}".format(ratio)
            child.size = child.size * ratio
            child.pos  = child.pos  * ratio
            if child.__class__ == WordsNode:
                try:
                    child.fontsize = child.fontsize * ratio
                except RuntimeError:
                    print("fontsize remained unchanged")

        self.old_size = self.size
        return True

    def resize(self, new_size):
        self.size = new_size
        self.resizeChildren(self.size)

    def scale(self, ratio):
        self.resize(self.size * ratio)


    # make sure size reflects the content of the div, right after every appendChild
    def getMediaSize(self):
        size = Point2D()
        for child in self.children:
            size.x = max( size.x, child.pos.x + child.size.x )
            size.y = max( size.y, child.pos.y + child.size.y )
        return size

    # reset the size, according to content
    def appendChild(self, node):
        #print "appending Child"
        super(WidgetBase, self).appendChild(node)
        if self.getMediaSize().x > 0 and self.getMediaSize().y > 0:
            self.old_size = self.size = self.getMediaSize()


    def fillParent(self, size = None):
        # takes size only for SIZE_CHANGED callback
        #self.DYNAMIC_SIZE = False
        self.fillParentV()
        self.fillParentH()

    def fillParentV(self, size = None):
        #self.DYNAMIC_SIZE = False
        self.y = 0
        self.height = self.parent.height
        if self.background:
            self.background.size = self.background.size.x, self.parent.height

    def fillParentH(self, size = None):
        #self.DYNAMIC_SIZE = False
        self.x = 0
        self.width = self.parent.width
        if self.background:
            self.background.size = self.parent.width, self.background.size.y

    def snapToBottom(self, other = None):
        if other is None:
            other = self.parent
        self.y = other.y+other.height - self.height
