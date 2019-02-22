import itertools


class Icosahedron:
    def __init__(self, n, cell_class):
        self._cell_class = cell_class
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
            return self._cell_class(x, y)
        else:
            return None

    def _pos_exists(self, pos):
        """ Boolean indicator of cell existence. """
        N = self.N
        x, y = pos
        if y < 3*N:
            xx = x % (6 * N)
            if xx <= 3*N:
                if xx > y:
                    return False
            else:
                if 6*N-xx > y:
                    return False
        elif y >= 6*N:
            xx = x % (6 * N)
            yy = y % (6 * N)
            if xx <= 3*N:
                if xx <= yy:
                    return False
            else:
                if 6*N-xx <= yy:
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
