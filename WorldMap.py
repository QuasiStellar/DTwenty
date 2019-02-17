import arcade

import Game
import Cell


class WorldMap(object):

    def __init__(self):
        self.map = [[Cell.Cell(i, j) for j in range(9 * Game.N)] for i in range(30 * Game.N)]

    def tectonic(self, plate_count):
        num = 1
        plate_centers = {}
        for i in range(plate_count):
            random_cell = Cell.Cell.random_cell()
            while random_cell in plate_centers:
                random_cell = Cell.Cell.random_cell()
            self.map[random_cell[0]][random_cell[1]].plate = num
            self.map[random_cell[0]][random_cell[1]].color = arcade.color.RED
            num += 1
