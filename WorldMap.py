import arcade

import Game
import Cell


class WorldMap(object):

    def __init__(self):
        self.map = [[Cell.Cell(x, y) for y in range(9 * Game.N)] for x in range(30 * Game.N)]

    def tectonic(self, plate_count):
        num = 1
        plate_centers = {}
        for i in range(plate_count):
            random_cell = Cell.Cell.random_cell()
            while random_cell in plate_centers:
                random_cell = Cell.Cell.random_cell()
            x, y = random_cell
            self.map[x][y].plate = num
            self.map[x][y].color = arcade.color.RED
            num += 1
