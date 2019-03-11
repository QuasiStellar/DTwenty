from collections import namedtuple
from random import Random


class VertexMap(object):

    def __init__(self, cells_on_edge, vertex_class, seed):
        self.cells_on_edge = cells_on_edge
        self._vertex_class = vertex_class
        x_size = 10 * self.cells_on_edge
        y_size = self.cells_on_edge + 1
        self.vertex_list = [[self.__create_vertex(x, imag_y) for imag_y in range(y_size)]
                            for x in range(x_size)]
        self.random = Random(seed)

    def __create_vertex(self, x, imag_y):
        y = self.__get_real_y(x, imag_y)
        pos = (x, y)
        return self._vertex_class(pos)

    def __getitem__(self, pos):
        x, y = pos
        imag_y = self.__get_imaginary_y(x, y)
        return self.vertex_list[x][imag_y]

    def __get_real_y(self, x, imaginary_y):
        """ Returns real vertex height based on vertex_list height. """
        edge = self.cells_on_edge
        xx = x % (edge * 2)
        bottom_indent = min(xx, 2 * edge - xx)
        return bottom_indent + imaginary_y * 2

    def __get_imaginary_y(self, x, real_y):
        """ Returns vertex_list height based on real vertex height. """
        edge = self.cells_on_edge
        xx = x % (edge * 2)
        bottom_indent = min(xx, 2 * edge - xx)
        return (real_y - bottom_indent) // 2

    def __get_distance(self, ver_a, ver_b):
        """ Returns distance between two vertexes. """
        x1, y1 = ver_a.pos
        x2, y2 = ver_b.pos
        if y1 == y2:
            return abs(x1 - x2) // 2
        else:
            return abs(y1 - y2)

    def __get_middle(self, ver_a, ver_b):
        """ Returns a vertex between two given. """
        x1, y1 = ver_a.pos
        x2, y2 = ver_b.pos
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        return self[x, y]

    def define_angular_vertexes(self):
        pass

    def emerald(self, ver_a, ver_b, ver_c):
        """ Find all vertexes' height. """
        distance = self.__get_distance(ver_a, ver_b)
        sigma = distance / self.cells_on_edge
        for ver_1, ver_2 in ((ver_a, ver_b), (ver_b, ver_c), (ver_a, ver_c)):
            ver_mid = self.__get_middle(ver_1, ver_2)
            ver_mid.height = (ver_1.height + ver_2.height) / 2 + self.random.gauss(0, sigma)
        if distance != 2:
            ver_ab = self.__get_middle(ver_a, ver_b)
            ver_bc = self.__get_middle(ver_b, ver_c)
            ver_ac = self.__get_middle(ver_a, ver_c)
            self.emerald(ver_a, ver_ab, ver_ac)
            self.emerald(ver_b, ver_ab, ver_bc)
            self.emerald(ver_c, ver_bc, ver_ac)
            self.emerald(ver_ab, ver_bc, ver_ac)

    def vertexes_by_cell(self, cell):
        cell_x, cell_y = cell.pos
        _List = namedtuple("List", "vertical left right")
        x_list = _List(
            left=cell_x - 1,
            vertical=cell_x,
            right=cell_x + 1
        )
        if cell.world_map.is_upside_down(cell):
            y_list = _List(
                vertical=cell_y,
                left=cell_y + 1,
                right=cell_y + 1
            )
        else:
            y_list = _List(
                vertical=cell_y + 1,
                left=cell_y - 1,
                right=cell_y - 1
            )
        positions_list = zip(x_list, y_list)
        vertex_list = map(lambda pos: self[pos], positions_list)
        return tuple(vertex_list)
