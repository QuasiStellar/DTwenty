import arcade
import random

import Cell
import Icosahedron
import TectonicPlate


# Low numbers slow down plate forming,
# while high makes distances from the border to the plate centers similar.
OVERGROWTH_FACTOR = 0.5


class WorldMap(Icosahedron.Icosahedron):

    def __init__(self, n):
        super().__init__(n, cell_class=Cell.Cell)

    def tectonic_generation(self, plate_count):
        # already_in_plate - set of all marked cells (represented as coordinates tuples).
        already_in_plate = set()
        # border_cells - set of cells which have undistributed neighbours.
        border_cells = set()
        # plates - list of TectonicPlates
        plates = []
        # plate_centers consists of centers' coordinates tuples.
        plate_centers = random.sample(self.cells, plate_count)
        plate_centers = map(lambda c: (c.x, c.y), plate_centers)
        # Plate centers determination.
        for plate_index, plate_center in enumerate(plate_centers):
            new_plate = TectonicPlate.TectonicPlate(plate_index)
            plates.append(new_plate)
            new_plate.cells.add(plate_center)
            new_plate.overgrowth_factor = random.random()
            already_in_plate.add(plate_center)
            border_cells.add(plate_center)
            x, y = plate_center
            self._map[x][y].plate = plate_index
            self._map[x][y].color = arcade.color.RED
        # Other cells distribution.
        while len(already_in_plate) != 180 * self.N ** 2:
            for pos in tuple(border_cells):
                cell_itself = self._map[pos[0]][pos[1]]
                plate = cell_itself.plate
                any_neighbours = False
                for near_cell in self.near_cells(pos):
                    near_pos = (near_cell.x, near_cell.y)
                    if near_pos not in already_in_plate:
                        any_neighbours = True
                        if random.random() < plates[plate].overgrowth_factor:
                            already_in_plate.add(near_pos)
                            border_cells.add(near_pos)
                            plates[plate].cells.add(near_pos)
                            x, y = near_pos
                            self._map[x][y].plate = plate
                            self._map[x][y].color = (100 + 5*plate, 100 + 5*plate, 100 + 5*plate)
                if not any_neighbours:
                    border_cells.remove(pos)
