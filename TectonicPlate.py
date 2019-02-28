class TectonicPlate(object):

    def __init__(self, index, world_map):
        self.index = index
        self.world_map = world_map
        self.cells = set()
        self.overgrowth_factor = 1

    def add_pos(self, pos):
        self.cells.add(pos)
        cell = self.world_map[pos]
        cell.plate = self.index
        cell.tectonic_color = (100 + 30 * self.index,) * 3

    @property
    def size(self):
        return len(self.cells)
