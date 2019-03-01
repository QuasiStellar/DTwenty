import random

from Cell import Cell
from Icosahedron import Icosahedron
from TectonicPlate import TectonicPlate


class WorldMap(Icosahedron):

    def __init__(self, n, tectonic_plates_count, seed):
        super().__init__(cells_on_edge=2**n, cell_class=Cell)
        self.tectonic_plates_count = tectonic_plates_count
        # TODO: localize
        random.seed(seed)

    def tectonic_generation(self):
        plate_count = self.tectonic_plates_count
        # plate_centers consists of centers' coordinates tuples
        plate_centers = random.sample(self.cells, plate_count)

        # plates - list of TectonicPlates
        plates = []

        # plates initialization
        for plate_index, plate_center in enumerate(plate_centers):
            new_plate = TectonicPlate(plate_index, self)
            new_plate.overgrowth_factor = random.random()/4*3 + 0.25  # 0.25 - 0.75
            new_plate.add_cell(plate_center)
            plates.append(new_plate)

        # already_in_plate - set of all marked cells (represented as coordinates tuples)
        already_in_plate = set(plate_centers)
        # border_cells - set of cells which have undistributed neighbours
        border_cells = set(plate_centers)

        # Other cells distribution.
        while len(already_in_plate) != len(self.cells):
            for cell in tuple(border_cells):
                plate_index = cell.plate
                plate = plates[plate_index]
                cells_near = self.get_cells_near(cell)
                cells_near = set(cells_near)
                # difference_update is slower than difference there
                cells_near = cells_near - already_in_plate
                for near_cell in tuple(cells_near):
                    if random.random() < plate.overgrowth_factor:
                        plate.add_cell(near_cell)
                        already_in_plate.add(near_cell)
                        border_cells.add(near_cell)
                        cells_near.remove(near_cell)
                if not cells_near:
                    border_cells.remove(cell)
