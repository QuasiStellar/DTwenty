class VertexMap(object):

    def __init__(self, cells_on_edge, vertex_class):
        self.cells_on_edge = cells_on_edge
        self._vertex_class = vertex_class
        x_size = 10 * self.cells_on_edge
        y_size = self.cells_on_edge + 1
        self.vortex_list = [[self._vertex_class(x, y) for y in range(y_size)]
                            for x in range(x_size)]

