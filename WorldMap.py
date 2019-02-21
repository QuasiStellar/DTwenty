import arcade
import itertools
import random

import Cell

# Low numbers slow down plate forming, while high makes distances from the border to the plate centers similar.
OVERGROWTH_FACTOR = 0.5


class WorldMap:

    def __init__(self, n):
        self.N = n
        # map - 2-dim list of existing cells.
        self._map = [[self.__create_cell(x, y) for y in range(9 * self.N)] for x in range(30 * self.N)]
        # cells - tuple of all cells.
        cells = itertools.chain(*self._map)  # join columns
        cells = filter(lambda c: c is not None, cells)
        self.cells = tuple(cells)

    def __create_cell(self, x, y):
        """ create_cell - Cell object for existing cells. """
        if self._pos_exists((x, y)):
            return Cell.Cell(x, y)
        else:
            return None

    def _pos_exists(self, pos):
        """ Boolean indicator of cell existence. """
        x, y = pos
        if y < 3*self.N:
            xx = x % (6 * self.N)
            if xx <= 3*self.N:
                if xx > y:
                    return False
            else:
                if 6*self.N-xx > y:
                    return False
        elif y >= 6*self.N:
            xx = x % (6 * self.N)
            yy = y % (6 * self.N)
            if xx <= 3*self.N:
                if xx <= yy:
                    return False
            else:
                if 6*self.N-xx <= yy:
                    return False
        return True

    def get_directions(self, x, y):
        """ Returns tuple of possible directions. """
        N = self.N
        xx = x % (6 * N)
        yy = y % (6 * N)
        if (x + y) % 2 == 0:
            if y == 0:
                return [(-6*N, 0),
                        (6*N, 0),
                        (0, 1)]
            if xx == yy and y < 3*N:
                return [(-1, 0),
                        (2*(3*N-yy), 0),
                        (0, 1)]
            if (6*N - xx) == yy and y < 3*N:
                return [(-2*(3*N-yy), 0),
                        (1, 0),
                        (0, 1)]
            return [(-1, 0), (1, 0), (0, 1)]
        else:
            if y == 9*N - 1:
                return [(-6*N, 0),
                        (6 * N, 0),
                        (0, -1)]
            if xx-1 == yy and y >= 6*N:
                return [(-2*(yy+1), 0),
                        (1, 0),
                        (0, -1)]
            if (6*N - xx - 1) == yy and y >= 6*N:
                return [(-1, 0),
                        (2 * (yy + 1), 0),
                        (0, -1)]
            return [(-1, 0), (1, 0), (0, -1)]

    def near_cells(self, coord):
        """ Returns tuple of adjacent cells. """
        directions = self.get_directions(*coord)
        positions_near = map(lambda d: ((coord[0]+d[0]) % (30*self.N), coord[1]+d[1]), directions)
        cells_near = map(lambda pos: self._map[pos[0]][pos[1]], positions_near)
        return tuple(cells_near)

    def tectonic(self, plate_count):
        # already_in_plate - set of all marked cells (represented as coordinates tuples).
        already_in_plate = set()
        # border_cells - set of cells which have undistributed neighbours.
        border_cells = set()
        # plate represented as set of coordinates tuples
        plates = []
        # plate_centers consists of centers' coordinates tuples.
        plate_centers = random.sample(self.cells, plate_count)
        plate_centers = map(lambda c: (c.x, c.y), plate_centers)
        # Plate centers determination.
        for plate_index, plate_center in enumerate(plate_centers):
            plates.append({plate_center})
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
                        if random.random() < OVERGROWTH_FACTOR:
                            already_in_plate.add(near_pos)
                            border_cells.add(near_pos)
                            plates[plate].add(near_pos)
                            x, y = near_pos
                            self._map[x][y].plate = plate
                            self._map[x][y].color = (100 + 5*plate, 100 + 5*plate, 100 + 5*plate)
                if not any_neighbours:
                    border_cells.remove(pos)
