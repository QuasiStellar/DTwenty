import collections
import itertools


_Size = collections.namedtuple("Size", "x y")
_Directions = collections.namedtuple("Directions", "left right middle")


class Icosahedron:

    def __init__(self, cells_on_edge, cell_class):
        self.cells_on_edge = cells_on_edge
        self._cell_class = cell_class
        x_size = 10*self.cells_on_edge
        y_size = 3*self.cells_on_edge
        self.size = _Size(x_size, y_size)
        # map - 2-dim list of existing cells
        self._map = [[self.__create_cell((x, y)) for y in range(y_size)]
                     for x in range(x_size)]
        # cells - tuple of all cells.
        cells = itertools.chain(*self._map)  # join columns
        cells = filter(lambda c: c is not None, cells)
        self.cells = tuple(cells)

    def __getitem__(self, pos):
        x, y = pos
        return self._map[x][y]

    def __create_cell(self, pos):
        """ Returns cell object for existing cells. """
        if self._pos_exists(pos):
            return self._cell_class(pos, world_map=self)
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

    def is_upside_down(self, cell):
        if isinstance(cell, self._cell_class):
            x, y = cell.x, cell.y
        else:
            # TODO: replace positions with cells everywhere
            x, y = cell
        return (x + y) % 2 == 0

    # TODO: remove or make private
    def get_positions_near(self, x, y):
        """ Returns tuple of possible directions. """
        pos = (x, y)
        if not self._pos_exists(pos):
            raise IndexError
        width = self.size.x
        left = ((x-1) % width, y)
        right = ((x+1) % width, y)
        cell_upside_down = self.is_upside_down(pos)
        if cell_upside_down:
            middle = (x, y+1)
        else:
            middle = (x, y-1)
        face_height = self.cells_on_edge
        yy = y % face_height
        if y < face_height:
            border_distance = 2 * (face_height - yy)
        elif y >= 2*face_height:
            border_distance = 2 * (yy + 1)
        else:
            border_distance = None
        if not self._pos_exists(left):
            left = ((x-border_distance) % width, y)
        if not self._pos_exists(right):
            right = ((x+border_distance) % width, y)
        return _Directions(left=left, right=right, middle=middle)

    def get_cells_near(self, cell):
        """ Returns tuple of adjacent cells. """
        positions_near = self.get_positions_near(cell.x, cell.y)
        cells_near = map(lambda pos: self[pos], positions_near)
        return _Directions(cells_near)
