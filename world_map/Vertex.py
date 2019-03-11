from collections import namedtuple


_Pos = namedtuple("Pos", "x y")


class Vertex(object):

    def __init__(self, pos):
        self.pos = _Pos(*pos)
        self.height = 0
