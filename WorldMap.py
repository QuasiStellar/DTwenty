import arcade
import random

import Cell
import Icosahedron


# Low numbers slow down plate forming, while high makes plates similar.
OVERGROWTH_FACTOR = 0.5


class WorldMap(Icosahedron.Icosahedron):

    def __init__(self, n):
        super().__init__(n, cell_class=Cell.Cell)

    def tectonic(self, plate_count):
        # already_in_plate - set of all marked cells (represented as coordinates tuples).
        already_in_plate = set()
        # plate represented as set of coordinates tuples
        plates = []
        # plate_centers consists of centers' coordinates tuples.
        plate_centers = random.sample(self.cells, plate_count)
        plate_centers = map(lambda c: (c.x, c.y), plate_centers)
        # Plate centers determination.
        for plate_index, plate_center in enumerate(plate_centers):
            plates.append({plate_center})
            already_in_plate.add(plate_center)
            x, y = plate_center
            self._map[x][y].plate = plate_index
            self._map[x][y].color = arcade.color.RED
        # Other cells distribution.
        while len(already_in_plate) != 180 * self.N ** 2:
            for pos in tuple(already_in_plate):
                cell_itself = self._map[pos[0]][pos[1]]
                plate = cell_itself.plate
                for near_cell in self.near_cells(pos):
                    near_pos = (near_cell.x, near_cell.y)
                    if near_pos not in already_in_plate:
                        if random.random() < OVERGROWTH_FACTOR:
                            already_in_plate.add(near_pos)
                            plates[plate].add(near_pos)
                            x, y = near_pos
                            self._map[x][y].plate = plate
                            self._map[x][y].color = (100 + 30*plate, 100 + 30*plate, 100 + 30*plate)
