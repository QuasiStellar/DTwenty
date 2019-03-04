class VertexMap(object):

    def __init__(self, cells_on_edge, vertex_class):
        self.cells_on_edge = cells_on_edge
        self._vertex_class = vertex_class
        x_size = 10 * self.cells_on_edge
        y_size = self.cells_on_edge + 1
        self.vertex_list = [[self._vertex_class(x, y) for y in range(y_size)]
                            for x in range(x_size)]

    def __real_y(self, x, imaginary_y):
        edge = self.cells_on_edge
        xx = x % (edge * 2)
        bottom_indent = min(xx, 2 * edge - xx)
        return bottom_indent + imaginary_y * 2

    def __imaginary_y(self, x, real_y):
        edge = self.cells_on_edge
        xx = x % (edge * 2)
        bottom_indent = min(xx, 2 * edge - xx)
        return (real_y - bottom_indent) // 2

    def middle(self, ver_a, ver_b):
        """ Find a vertex between two given. """
        x1 = ver_a.x
        y1 = ver_a.y
        x2 = ver_b.x
        y2 = ver_b.y
        # consider that vertexes are on the same line and have even distance between them
        real_y1 = self.__real_y(x1, y1)
        real_y2 = self.__real_y(x2, y2)
        real_y = (real_y1 + real_y2) // 2
        x = (x1 + x2) // 2
        y = self.__imaginary_y(x, real_y)
        return self.vertex_list[x][y]

    @staticmethod
    def vertexes_by_cell():
        pass
