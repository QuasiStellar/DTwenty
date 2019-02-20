import arcade
import itertools
import random

import Game
import Cell

""" Low numbers slow down plate forming, while high makes plates similar. """
OVERGROWTH_FACTOR = 0.5


class WorldMap(object):

    def __init__(self):
        """ map - 2-dim list of existing cells. """
        self._map = [[self.__create_cell(x, y) for y in range(9 * Game.N)] for x in range(30 * Game.N)]
        """ cells - tuple of all cells. """
        cells = itertools.chain(*self._map)
        cells = filter(lambda c: c is not None, cells)
        self.cells = tuple(cells)

    """ create_cell - Cell object for existing cells. """
    @classmethod
    def __create_cell(cls, x, y):
        if cls._pos_exists((x, y)):
            return Cell.Cell(x, y)
        else:
            return None

    """ Boolean indicator of cell existence. """
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

    """ Tuple of adjacent cells (for Q W E A D Z X C) """
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

    """ List of adjacent cells. """
    @staticmethod
    def near_cells(coord):
        near = WorldMap.get_directions(coord[0], coord[1])
        near_cells = map(lambda i: Game.world_map._map[coord[0]+near[i][0]][coord[1]+near[i][1]], range(8))
        return near_cells

    def tectonic(self, plate_count):

        """ positions - set of all marked cells (coordinates tuples). """
        positions = set()
        """ plates - list of sets of cells (coordinates tuples) in a plate. """
        plates = []
        """ plate_centers - set of centers' coordinates tuples. """
        plate_centers = random.sample(self.cells, plate_count)
        plate_centers = map(lambda c: (c.x, c.y), plate_centers)
        plate_centers = set(plate_centers)
        num = 1

        """ Plate centers determination. """
        for plate_center in plate_centers:
            """ plate_set - set of cells (coordinates tuples) used in plates. """
            plate_set = set()
            plate_set.add(plate_center)
            plates.append(set(plate_set))
            positions.add(plate_center)
            x, y = plate_center
            self._map[x][y].plate = num
            self._map[x][y].color = arcade.color.RED
            num += 1

        """ Other cells distribution. """
        while len(positions) != 180 * Game.N ** 2:
            for pos in tuple(positions):
                """ cell_itself - selected cell. """
                cell_itself = Game.world_map._map[pos[0]][pos[1]]
                plate = cell_itself.plate
                for near_cell in self.near_cells(pos):
                    """ new_pos - tuple of adjacent cell coordinates. """
                    near_pos = (near_cell.x, near_cell.y)
                    if near_pos not in positions:
                        if random.random() < OVERGROWTH_FACTOR:
                            positions.add(near_pos)
                            plates[plate].add(near_pos)
                            x, y = near_pos
                            self._map[x][y].plate = plate
                            self._map[x][y].color = arcade.color.BLUE
