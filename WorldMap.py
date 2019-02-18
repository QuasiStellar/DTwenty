import arcade
import itertools
import random

import Game
import Cell

OVERGROWTH_FACTOR = 0.5


class WorldMap(object):

    def __init__(self):
        create_cell = lambda x, y: Cell.Cell(x, y) if self._pos_exists((x, y)) else None
        self._map = [[create_cell(x, y) for y in range(9 * Game.N)] for x in range(30 * Game.N)]
        cells = itertools.chain(*self._map)  # join columns
        cells = filter(lambda c: c is not None, cells)
        self.cells = tuple(cells)

    @staticmethod
    def _pos_exists(pos):
        x, y = pos
        if y < 3*Game.N:
            xx = x % (6 * Game.N)
            if xx <= 3*Game.N:
                if xx > y:
                    return False
            else:
                if 6*Game.N-xx > y:
                    return False
        elif y >= 6*Game.N:
            xx = x % (6 * Game.N)
            yy = y % (6 * Game.N)
            if xx <= 3*Game.N:
                if xx <= yy:
                    return False
            else:
                if 6*Game.N-xx <= yy:
                    return False
        return True

    @staticmethod
    def get_directions(x, y):
        xx = x % (6 * Game.N)
        yy = y % (6 * Game.N)
        if (x + y) % 2 == 0:
            if y == 0:
                return [(-6*Game.N, 0),
                        (0, 0),
                        (6*Game.N, 0),
                        (-6*Game.N, 0),
                        (6*Game.N, 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            if xx == yy and y < 3*Game.N:
                return [(-1, 0),
                        (0, 0),
                        (2*(3*Game.N-yy), 0),
                        (-1, 0),
                        (2*(3*Game.N-yy), 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            if (6*Game.N - xx) == yy and y < 3*Game.N:
                return [(-2*(3*Game.N-yy), 0),
                        (0, 0),
                        (1, 0),
                        (-2*(3*Game.N-yy), 0),
                        (1, 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            return [(-1, 0), (0, 0), (1, 0), (-1, 0), (1, 0), (0, 1), (0, 1), (0, 1)]
        else:
            if y == 9*Game.N-1:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-6*Game.N, 0),
                        (6*Game.N, 0),
                        (-6*Game.N, 0),
                        (0, 0),
                        (6*Game.N, 0)]
            if xx-1 == yy and y >= 6*Game.N:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-2*(yy+1), 0),
                        (1, 0),
                        (-2*(yy+1), 0),
                        (0, 0),
                        (1, 0)]
            if (6*Game.N - xx - 1) == yy and y >= 6*Game.N:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-1, 0),
                        (2*(yy+1), 0),
                        (-1, 0),
                        (0, 0),
                        (2*(yy+1), 0)]
            return [(0, -1), (0, -1), (0, -1), (-1, 0), (1, 0), (-1, 0), (0, 0), (1, 0)]

    @staticmethod
    def near_cells(coord):
        near = WorldMap.get_directions(coord[0], coord[1])
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
