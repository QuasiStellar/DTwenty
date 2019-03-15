from random import Random

from color_modes.ColorMode import ColorMode


class CommonColorMode(ColorMode):

    def __init__(self, *, world_map):
        super().__init__(world_map=world_map)
        self._cells_colors = {}
        color_random = Random(self.world_map.seed)
        # random light-gray shade
        for cell in self.world_map.cells:
            random_color = color_random.randint(128, 256)
            self._cells_colors[cell] = (random_color,) * 3

    def get_cell_color(self, cell):
        return self._cells_colors[cell]
