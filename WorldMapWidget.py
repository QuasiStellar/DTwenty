import itertools

import arcade

from color_modes import CommonColorMode, HeightColorMode, TectonicColorMode


class WorldMapWidget:

    def __init__(self, world_map, size_px):
        self.world_map = world_map

        self.size_px = size_px

        width, height = size_px
        self.face_size_px = (width//5, height//3)

        face_width, face_height = self.face_size_px
        cells_on_edge = self.world_map.cells_on_edge
        self.cell_size_px = (face_width//cells_on_edge, face_height//cells_on_edge)

        # ShapeElementList object for borders drawing
        self._borders = arcade.ShapeElementList()

        face_width, face_height = self.face_size_px
        x_list = [face_width/2 * i for i in range(11)]
        y_list_1 = itertools.cycle([0*face_height, 1*face_height])
        y_list_2 = itertools.cycle([2*face_height, 3*face_height])
        point_list_1 = tuple(zip(x_list, y_list_1))
        point_list_2 = tuple(zip(x_list, y_list_2))

        # Borders drawing
        border_1 = arcade.create_line_strip(point_list_1, arcade.color.WHITE, 2)
        border_2 = arcade.create_line_strip(point_list_2, arcade.color.WHITE, 2)
        self._borders.append(border_1)
        self._borders.append(border_2)

        triangles = map(self._get_triangle_vertices, self.world_map.cells)
        triangles_vertices = itertools.chain.from_iterable(triangles)
        self._cells_vertices = list(triangles_vertices)

        # ShapeElementList object for cells drawing. See _update_cells_colors()
        self._cells_grid_container = None

        self._color_modes = {
            "common": CommonColorMode(world_map=world_map),
            "height": HeightColorMode(world_map=world_map),
            "tectonic": TectonicColorMode(world_map=world_map)
        }

        self._color_mode = None
        self.set_color_mode("common")

    def on_draw(self):
        self._cells_grid_container.draw()
        self._borders.draw()

    @property
    def color_mode_name(self):
        for name, color_mode in self._color_modes.items():
            if color_mode is self._color_mode:
                return name

    def set_color_mode(self, color_mode_name):
        color_mode = self._color_modes[color_mode_name]
        if not color_mode.can_be_enabled():
            raise AssertionError("that color mode can't be enabled now: %s" % color_mode_name)
        self._color_mode = color_mode
        self._update_cells_colors()

    def _update_cells_colors(self):
        """ Map visual part update. """
        color_list = []

        # Colors recalculation.
        for cell in self.world_map.cells:
            color = self._color_mode.get_cell_color(cell)
            color_list.extend(3 * [color])

        self._cells_grid_container = arcade.ShapeElementList()
        cells_grid = arcade.create_triangles_filled_with_colors(self._cells_vertices, color_list)
        self._cells_grid_container.append(cells_grid)

    def _get_triangle_vertices(self, cell):
        """ Returns tuple of vertex coordinates. """
        x, y = cell.pos
        middle_x = x / 2
        left_x = middle_x - 0.5
        right_x = middle_x + 0.5
        vertices_x = (left_x, right_x, middle_x)
        down_y = y
        up_y = y + 1
        cell_upside_down = self.world_map.is_upside_down(cell)
        if cell_upside_down:
            vertices_y = (up_y, up_y, down_y)
        else:
            vertices_y = (down_y, down_y, up_y)
        triangle = zip(vertices_x, vertices_y)
        triangle = list(triangle)

        cell_width, cell_height = self.cell_size_px
        for vertex_index, vertex in enumerate(tuple(triangle)):
            x, y = vertex
            vertex = (x * cell_width, y * cell_height)
            vertex = map(round, vertex)
            triangle[vertex_index] = tuple(vertex)
        return tuple(triangle)
