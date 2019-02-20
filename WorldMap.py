import arcade
import itertools
import random

import Cell

OVERGROWTH_FACTOR = 0.5


class WorldMap:

    def __init__(self, N):
        self.N = N
        create_cell = lambda x, y: (Cell.Cell(x, y) if self._pos_exists((x, y)) else None)
        self._map = [[create_cell(x, y) for y in range(9 * self.N)] for x in range(30 * self.N)]
        cells = itertools.chain(*self._map)  # join columns
        cells = filter(lambda c: c is not None, cells)
        self.cells = tuple(cells)

    def _pos_exists(self, pos):
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
        N = self.N
        xx = x % (6 * N)
        yy = y % (6 * N)
        if (x + y) % 2 == 0:
            if y == 0:
                return [(-6*N, 0),
                        (0, 0),
                        (6*N, 0),
                        (-6*N, 0),
                        (6*N, 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            if xx == yy and y < 3*N:
                return [(-1, 0),
                        (0, 0),
                        (2*(3*N-yy), 0),
                        (-1, 0),
                        (2*(3*N-yy), 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            if (6*N - xx) == yy and y < 3*N:
                return [(-2*(3*N-yy), 0),
                        (0, 0),
                        (1, 0),
                        (-2*(3*N-yy), 0),
                        (1, 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            return [(-1, 0), (0, 0), (1, 0), (-1, 0), (1, 0), (0, 1), (0, 1), (0, 1)]
        else:
            if y == 9*N - 1:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-6*N, 0),
                        (6*N, 0),
                        (-6*N, 0),
                        (0, 0),
                        (6*N, 0)]
            if xx-1 == yy and y >= 6*N:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-2*(yy+1), 0),
                        (1, 0),
                        (-2*(yy+1), 0),
                        (0, 0),
                        (1, 0)]
            if (6*N - xx - 1) == yy and y >= 6*N:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-1, 0),
                        (2*(yy+1), 0),
                        (-1, 0),
                        (0, 0),
                        (2*(yy+1), 0)]
            return [(0, -1), (0, -1), (0, -1), (-1, 0), (1, 0), (-1, 0), (0, 0), (1, 0)]

    def near_cells(self, coord):
        directions = self.get_directions(*coord)
        positions_near = map(lambda d: (coord[0]+d[0], coord[1]+d[1]), directions)
        cells_near = map(lambda pos: self._map[pos[0]][pos[1]], positions_near)
        return cells_near

    def tectonic(self, plate_count):
        already_in_plate = set()
        plates = []
        plate_centers = random.sample(self.cells, plate_count)
        plate_centers = map(lambda c: (c.x, c.y), plate_centers)
        for plate_index, plate_center in enumerate(plate_centers):
            plates.append({plate_center})
            already_in_plate.add(plate_center)
            x, y = plate_center
            num = 1 + plate_index
            self._map[x][y].plate = num
            self._map[x][y].color = arcade.color.RED
        while len(already_in_plate) != 180 * self.N ** 2:
            for pos in tuple(already_in_plate):
                cell_itself = self._map[pos[0]][pos[1]]
                plate = cell_itself.plate
                for near_cell in self.near_cells(pos):
                    near_pos = (near_cell.x, near_cell.y)
                    if near_pos not in already_in_plate:
                        if random.random() < OVERGROWTH_FACTOR:
                            already_in_plate.add(near_pos)
                            plates[plate].add(near_pos)
                            x, y = near_pos
                            self._map[x][y].plate = plate
                            self._map[x][y].color = arcade.color.BLUE
