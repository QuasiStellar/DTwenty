from collections import namedtuple


_Pos = namedtuple("Pos", "x y")


class Cell(object):

    def __init__(self, pos, *, world_map):
        self.world_map = world_map
        self.pos = _Pos(*pos)
        self.type = 0
        self.temperature = 0
        self.height = 0
        self.plate = 0

        # TODO: split logic and output
        # random light-gray shade
        random_color = self.world_map.color_random.randint(128, 256)
        self.color = (random_color, random_color, random_color)

        self.tectonic_color = self.color

        self.height_color = self.color
