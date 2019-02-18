import arcade
import random

import Game
import Cell

OVERGROWTH_FACTOR = 0.5


class WorldMap(object):

    def __init__(self):
        self.map = [[Cell.Cell(x, y) for y in range(9 * Game.N)] for x in range(30 * Game.N)]

    @staticmethod
    def near_cells(coord):
        near = Cell.Cell.near(coord[0], coord[1])
        near_cells = map(lambda i: Game.world_map.map[coord[0]+near[i][0]][coord[1]+near[i][1]], (i for i in range(8)))
        return near_cells

    def tectonic(self, plate_count):
        num = 1
        plate_centers = set()
        cells = set()
        plates = []
        for i in range(plate_count):
            random_cell = Cell.Cell.random_cell()
            while random_cell in plate_centers:
                random_cell = Cell.Cell.random_cell()
            plate_centers.add(random_cell)
            plate_set = set()
            plate_set.add(random_cell)
            plates.append(set(plate_set))
            cells.add(random_cell)
            x, y = random_cell
            self.map[x][y].plate = num
            self.map[x][y].color = arcade.color.RED
            num += 1
        while len(cells) != 180 * Game.N ** 2:
            for cell in cells:
                for near_cell in self.near_cells(cell):
                    if near_cell not in cells:
                        if random.random() < OVERGROWTH_FACTOR:
                            cells.add(near_cell)
                            cell_itself = Game.world_map.map[cell[0]][cell[1]]
                            plates[cell_itself.plate].add(near_cell)
                            self.map[near_cell.x][near_cell.y].plate = cell_itself.plate
                            self.map[near_cell.x][near_cell.y].color = arcade.color.BLUE
