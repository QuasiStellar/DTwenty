import random

from Cell import Cell
from Icosahedron import Icosahedron
from TectonicPlate import TectonicPlate


class WorldMap(Icosahedron):

    def __init__(self, n, tectonic_plates_count, seed):
        super().__init__(cells_on_edge=2**n, cell_class=Cell)
        self.tectonic_plates_count = tectonic_plates_count
        random.seed(seed)

    def tectonic_generation(self):
        plate_count = self.tectonic_plates_count
        # plate_centers consists of centers' coordinates tuples
        plate_centers = random.sample(self.cells, plate_count)
        plate_centers = tuple(map(lambda c: (c.x, c.y), plate_centers))

        # plates - list of TectonicPlates
        plates = []

        # plates initialization
        for plate_index, plate_center in enumerate(plate_centers):
            new_plate = TectonicPlate(plate_index, self)
            new_plate.overgrowth_factor = random.random()/4*3 + 0.25  # 0.25 - 0.75
            new_plate.add_pos(plate_center)
            plates.append(new_plate)

        # already_in_plate - set of all marked cells (represented as coordinates tuples)
        already_in_plate = set(plate_centers)
        # border_cells - set of cells which have undistributed neighbours
        border_cells = set(plate_centers)

        # Other cells distribution.
        while len(already_in_plate) != len(self.cells):
            for pos in tuple(border_cells):
                plate_index = self[pos].plate
                plate = plates[plate_index]
                cells_near = self.near_cells(pos)
                positions_near = map(lambda c: (c.x, c.y), cells_near)
                positions_near = set(positions_near)
                positions_near = positions_near - already_in_plate  # difference_update is slower than difference there
                for near_pos in tuple(positions_near):
                    if random.random() < plate.overgrowth_factor:
                        plate.add_pos(near_pos)
                        already_in_plate.add(near_pos)
                        border_cells.add(near_pos)
                        positions_near.remove(near_pos)
                if not positions_near:
                    border_cells.remove(pos)
