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

    def __real_y_coordinate(self, vertex):
        """ Returns real vertex coordinates. """
        x = vertex.x
        y = vertex.y
        # consider that vertexes are on the same line and have even distance between them
        real_y = self.__real_y(x, y)
        real_coordinate = real_y
        return real_coordinate

    def __distance(self, ver_a, ver_b):
        """ Returns distance between two vertexes. """
        x1 = ver_a.x
        x2 = ver_b.x
        real_y1, real_y2 = self.__real_y_coordinate(ver_a), self.__real_y_coordinate(ver_b)
        if real_y1 == real_y2:
            return abs(x1 - x2) // 2
        else:
            return abs(real_y1 - real_y2)

    def __middle(self, ver_a, ver_b):
        """ Returns a vertex between two given. """
        x1 = ver_a.x
        x2 = ver_b.x
        real_y1, real_y2 = self.__real_y_coordinate(ver_a), self.__real_y_coordinate(ver_b)
        real_y = (real_y1 + real_y2) // 2
        x = (x1 + x2) // 2
        y = self.__imaginary_y(x, real_y)
        return self.vertex_list[x][y]

    def define_angular_vertexes(self):
        pass

    def emerald(self, ver_a, ver_b, ver_c):
        ver_ab = self.__middle(ver_a, ver_b)
        ver_bc = self.__middle(ver_b, ver_c)
        ver_ac = self.__middle(ver_a, ver_c)
        sigma = self.__distance(ver_a, ver_b) / self.cells_on_edge
        ver_ab.height = (ver_a.height + ver_b.height) / 2 + self.random.gauss(0, sigma)
        ver_bc.height = (ver_b.height + ver_c.height) / 2 + self.random.gauss(0, sigma)
        ver_ac.height = (ver_a.height + ver_c.height) / 2 + self.random.gauss(0, sigma)
        self.emerald(ver_a, ver_ab, ver_ac)
        self.emerald(ver_b, ver_ab, ver_bc)
        self.emerald(ver_c, ver_bc, ver_ac)
        self.emerald(ver_ab, ver_bc, ver_ac)

    @staticmethod
    def vertexes_by_cell():
        pass
