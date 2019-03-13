import itertools
import random

import arcade


class WorldMapWidget:

    def __init__(self, world_map, size_px):
        self.world_map = world_map

        self.size_px = size_px

        width, height = size_px
        self.face_size_px = (width//5, height//3)

        face_width, face_height = self.face_size_px
        cells_on_edge = self.world_map.cells_on_edge
        self.cell_size_px = (face_width//cells_on_edge, face_height//cells_on_edge)

        self._initialize_default_cells_colors()
        self._color_mode = 'common'

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
        self._update_cells_colors()

    def on_draw(self):
        self._cells_grid_container.draw()
        self._borders.draw()

    def set_color_mode(self, color_mode):
        if color_mode not in ("common", "tectonic", "height"):
            raise ValueError("is not color mode: %s" % color_mode)
        if color_mode == "tectonic":
            if not self.world_map.tectonic_plates_generated:
                raise AssertionError("tectonic plates are not generated yet")
        self._color_mode = color_mode
        self._update_cells_colors()

    @property
    def color_mode(self):
        return self._color_mode

    def _initialize_default_cells_colors(self):
        self._default_cells_colors = {}
        color_random = random.Random(self.world_map.seed)
        # random light-gray shade
        for cell in self.world_map.cells:
            random_color = color_random.randint(128, 256)
            self._default_cells_colors[cell] = (random_color,) * 3

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

    def _update_cells_colors(self):
        """ Map visual part update. """
        color_list = []

        # Colors recalculation.
        for cell in self.world_map.cells:
            color = self._get_cell_color(cell)
            color_list.extend(3 * [color])

        self._cells_grid_container = arcade.ShapeElementList()
        cells_grid = arcade.create_triangles_filled_with_colors(self._cells_vertices, color_list)
        self._cells_grid_container.append(cells_grid)

    def _get_cell_color(self, cell):
        if self.color_mode == "common":
            return self._default_cells_colors[cell]
        elif self.color_mode == "tectonic":
            min_color = 100
            max_color = 255
            max_plate_index = self.world_map.tectonic_plates_count - 1
            k = cell.plate.index / max_plate_index
            color = min_color + k*(max_color-min_color)
            return (int(color),) * 3
        elif self.color_mode == "height":
            # TODO
            return self._default_cells_colors[cell]
        else:
            raise AssertionError("Color mode does not exist: %s" % self.color_mode)
