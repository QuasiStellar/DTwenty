from collections import deque
from random import Random

from world_map.Cell import Cell
from world_map.Icosahedron import Icosahedron
from world_map.TectonicPlate import TectonicPlate


class WorldMap(Icosahedron):

    def __init__(self, n, tectonic_plates_count, submergence, seed):
        # TODO: split logic and output
        self.color_random = Random(seed)
        super().__init__(cells_on_edge=2**n, cell_class=Cell)
        self.tectonic_plates_count = tectonic_plates_count
        self.submergence = submergence
        self.random = Random(seed)

    def tectonic_generation(self):
        plate_centers = self.random.sample(self.cells, self.tectonic_plates_count)

        # plates - list of TectonicPlates
        plates = []

        # plates initialization
        for plate_index, plate_center in enumerate(plate_centers):
            new_plate = TectonicPlate(plate_index, self)
            new_plate.overgrowth_factor = self.random.random()/4*3 + 0.25  # 0.25 - 0.75
            new_plate.add_cell(plate_center)
            plates.append(new_plate)

        # already_in_plate - set of all marked cells
        already_in_plate = set(plate_centers)
        # border_cells - deque of cells which have undistributed neighbours
        border_cells = deque(plate_centers)

        # other cells distribution
        while len(already_in_plate) != len(self.cells):
            cell = border_cells.popleft()
            plate_index = cell.plate.index
            plate = plates[plate_index]
            cells_near = self.get_cells_near(cell)
            free_cells_near = filter(lambda c: c not in already_in_plate, cells_near)
            free_cells_near = list(free_cells_near)
            for near_cell in tuple(free_cells_near):
                if self.random.random() < plate.overgrowth_factor:
                    plate.add_cell(near_cell)
                    already_in_plate.add(near_cell)
                    border_cells.append(near_cell)
                    free_cells_near.remove(near_cell)
            if free_cells_near:
                border_cells.append(cell)
