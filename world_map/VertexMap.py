from collections import namedtuple
from itertools import starmap
from random import Random


class VertexMap(object):

    def __init__(self, cells_on_edge, vertex_class, seed):
        self.cells_on_edge = cells_on_edge
        self._vertex_class = vertex_class
        x_size = 10 * self.cells_on_edge
        y_size = self.cells_on_edge + 1
        self.vertex_list = [[self._vertex_class(x, y) for y in range(y_size)]
                            for x in range(x_size)]
        self.random = Random(seed)

    def __real_y(self, x, imaginary_y):
        """ Returns real vertex height based on vertex_list height. """
        edge = self.cells_on_edge
        xx = x % (edge * 2)
        bottom_indent = min(xx, 2 * edge - xx)
        return bottom_indent + imaginary_y * 2

    def __imaginary_y(self, x, real_y):
        """ Returns vertex_list height based on real vertex height. """
        edge = self.cells_on_edge
        xx = x % (edge * 2)
        bottom_indent = min(xx, 2 * edge - xx)
        return (real_y - bottom_indent) // 2

    def __distance(self, ver_a, ver_b):
        """ Returns distance between two vertexes. """
        x1 = ver_a.x
        x2 = ver_b.x
        real_y1, real_y2 = self.__real_y(ver_a.x, ver_a.y), self.__real_y(ver_b.x, ver_b.y)
        if real_y1 == real_y2:
            return abs(x1 - x2) // 2
        else:
            return abs(real_y1 - real_y2)

    def __middle(self, ver_a, ver_b):
        """ Returns a vertex between two given. """
        x1 = ver_a.x
        x2 = ver_b.x
        real_y1, real_y2 = self.__real_y(x1, ver_a.y), self.__real_y(x2, ver_b.y)
        real_y = (real_y1 + real_y2) // 2
        x = (x1 + x2) // 2
        y = self.__imaginary_y(x, real_y)
        return self.vertex_list[x][y]

    def define_angular_vertexes(self):
        pass

    def emerald(self, ver_a, ver_b, ver_c):
        """ Find all vertexes' height. """
        distance = self.__distance(ver_a, ver_b)
        sigma = distance / self.cells_on_edge
        for ver_1, ver_2 in ((ver_a, ver_b), (ver_b, ver_c), (ver_a, ver_c)):
            ver_mid = self.__middle(ver_1, ver_2)
            ver_mid.height = (ver_1.height + ver_2.height) / 2 + self.random.gauss(0, sigma)
        if distance != 2:
            ver_ab = self.__middle(ver_a, ver_b)
            ver_bc = self.__middle(ver_b, ver_c)
            ver_ac = self.__middle(ver_a, ver_c)
            self.emerald(ver_a, ver_ab, ver_ac)
            self.emerald(ver_b, ver_ab, ver_bc)
            self.emerald(ver_c, ver_bc, ver_ac)
            self.emerald(ver_ab, ver_bc, ver_ac)

    def vertexes_by_cell(self, cell):
        _List = namedtuple("List", "vertical left right")
        x_list = _List(
            left=cell.x - 1,
            vertical=cell.x,
            right=cell.x + 1
        )
        if cell.world_map.is_upside_down(cell):
            y_list = _List(
                vertical=cell.y,
                left=cell.y + 1,
                right=cell.y + 1
            )
        else:
            y_list = _List(
                vertical=cell.y + 1,
                left=cell.y - 1,
                right=cell.y - 1
            )
        positions_list = zip(x_list, y_list)
        y_list = starmap(self.__imaginary_y, positions_list)
        positions_list = zip(x_list, y_list)
        vertex_list = starmap(lambda x, y: self.vertex_list[x][y], positions_list)
        return tuple(vertex_list)
