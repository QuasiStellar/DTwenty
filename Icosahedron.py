import collections
import itertools


_Size = collections.namedtuple("Size", "x y")


class Icosahedron:
    def __init__(self, cells_on_edge, cell_class):
        self.cells_on_edge = cells_on_edge
        self._cell_class = cell_class
        x_size = 10*self.cells_on_edge
        y_size = 3*self.cells_on_edge
        self.size = _Size(x_size, y_size)
        # map - 2-dim list of existing cells
        self._map = [[self.__create_cell(x, y) for y in range(y_size)]
                     for x in range(x_size)]
        # cells - tuple of all cells.
        cells = itertools.chain(*self._map)  # join columns
        cells = filter(lambda c: c is not None, cells)
        self.cells = tuple(cells)

    def __getitem__(self, pos):
        x, y = pos
        return self._map[x][y]

    def __create_cell(self, x, y):
        """ Returns cell object for existing cells. """
        if self._pos_exists((x, y)):
            return self._cell_class(x, y)
        else:
            return None

    def _pos_exists(self, pos):
        """ Returns True if cell exist. """
        x, y = pos
        if not (0 <= x < self.size.x and 0 <= y < self.size.y):
            return False
        face_height = self.cells_on_edge
        period = 2*self.cells_on_edge
        xx = x % period
        if xx <= period/2:
            relative_y_border = xx
        else:
            relative_y_border = period - xx
        min_y = 0 + relative_y_border
        max_y = 2*face_height + relative_y_border - 1
        return min_y <= y <= max_y

    def get_directions(self, x, y):
        """ Returns tuple of possible directions. """
        pos = (x, y)
        if not self._pos_exists(pos):
            raise IndexError
        left = (-1, 0)
        right = (1, 0)
        horizontal_side_up = (x + y) % 2 == 0
        if horizontal_side_up:
            medium = (0, 1)
        else:
            medium = (0, -1)
        face_height = self.cells_on_edge
        yy = y % face_height
        if y < face_height:
            border_distance = 2 * (face_height - yy)
        elif y >= 2*face_height:
            border_distance = 2 * (yy + 1)
        else:
            border_distance = None
        sum_points = lambda a, b: ((a[0] + b[0]) % self.size.x, a[1] + b[1])
        if not self._pos_exists(sum_points(pos, left)):
            left = (-border_distance, 0)
        if not self._pos_exists(sum_points(pos, right)):
            right = (+border_distance, 0)
        return (left, right, medium)

    def near_cells(self, coord):
        """ Returns tuple of adjacent cells. """
        directions = self.get_directions(*coord)
        positions_near = map(lambda d: ((coord[0]+d[0]) % self.size.x, coord[1]+d[1]), directions)
        cells_near = map(lambda pos: self._map[pos[0]][pos[1]], positions_near)
        return tuple(cells_near)
