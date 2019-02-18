import arcade
import itertools
import random

import Game
import Cell

OVERGROWTH_FACTOR = 0.5


class WorldMap(object):

    def __init__(self):
        self._map = [[Cell.Cell(x, y) for y in range(9 * Game.N)] for x in range(30 * Game.N)]
        cells = itertools.chain(*self._map)  # join horizontals
        cells = filter(lambda c: c.exist, cells)
        self.cells = tuple(cells)

    @staticmethod
    def near_cells(coord):
        near = Cell.Cell.near(coord[0], coord[1])
        near_cells = map(lambda i: Game.world_map.map[coord[0]+near[i][0]][coord[1]+near[i][1]], (i for i in range(8)))
        return near_cells

    def tectonic(self, plate_count):
        cells = set()
        plates = []
        plate_centers = random.sample(self.cells, plate_count)
        plate_centers = map(lambda c: (c.x, c.y), plate_centers)
        plate_centers = set(plate_centers)
        num = 1
        for plate_center in plate_centers:
            plate_set = set()
            plate_set.add(plate_center)
            plates.append(set(plate_set))
            cells.add(plate_center)
            x, y = plate_center
            self._map[x][y].plate = num
            self._map[x][y].color = arcade.color.RED
            num += 1
        while len(cells) != 180 * Game.N ** 2:
            for cell in cells:
                for near_cell in self.near_cells(cell):
                    if near_cell not in cells:
                        if random.random() < OVERGROWTH_FACTOR:
                            cells.add(near_cell)
                            cell_itself = Game.world_map.map[cell[0]][cell[1]]
                            plates[cell_itself.plate].add(near_cell)
                            self._map[near_cell.x][near_cell.y].plate = cell_itself.plate
                            self._map[near_cell.x][near_cell.y].color = arcade.color.BLUE
