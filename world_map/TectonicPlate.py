class TectonicPlate(object):

    def __init__(self, index, world_map):
        self.index = index
        self.world_map = world_map
        self.cells = set()
        self.overgrowth_factor = 1
        is_oceanic = self.world_map.random.random() < self.world_map.submergence
        self.type = 'oceanic' if is_oceanic else 'continental'

    def add_cell(self, cell):
        self.cells.add(cell)
        cell.plate = self

    @property
    def size(self):
        return len(self.cells)
