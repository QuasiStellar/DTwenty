from collections import namedtuple


_Pos = namedtuple("Pos", "x y")


class Cell(object):

    def __init__(self, pos, *, world_map):
        self.world_map = world_map
        self.pos = _Pos(*pos)
        self.type = 0
        self.temperature = 0
        self.height = 0
        self.plate = None
