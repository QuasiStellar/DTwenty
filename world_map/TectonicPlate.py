import random


class TectonicPlate(object):

    def __init__(self, index, world_map):
        self.index = index
        self.world_map = world_map
        self.cells = set()
        self.overgrowth_factor = 1
        self.type = 'oceanic' if random.random() < self.world_map.submergence else 'continental'

    def add_cell(self, cell):
        self.cells.add(cell)
        cell.plate = self.index

    @property
    def size(self):
        return len(self.cells)
