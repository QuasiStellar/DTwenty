import itertools

import arcade

import Player
import WorldMap

VERSION = "alpha-0.3"
SCREEN_TITLE = "D20"


class Game(arcade.Window):

    def __init__(self, n, tectonic_plates_count, seed):
        # Size of the default window.
        self.SCREEN_WIDTH = 1500
        self.SCREEN_HEIGHT = 780
        self.FACE_SIZE = (300, 260)

        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False)

        # WorldMap object - main map.
        self.world_map = WorldMap.WorldMap(n, tectonic_plates_count, seed)
        self.cells_on_edge = self.world_map.cells_on_edge

        # Player object - a dot moving through the map.
        self.player = Player.Player(0, 0, self.world_map)

        # ShapeElementList object for borders drawing. See setup()
        self.borders = None

        # ShapeElementList object for cells drawing. See setup() & update_colors()
        self.cells = None

        self.hints_on = False
        self.hints_notification = True
        self.debug_mod = False
        self.display_player_coordinates = None

        self.mod = 'common'

        # List of dots for drawing.
        self.dot_list = []

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Map visual part setup."""
        face_width, face_height = self.FACE_SIZE

        self.borders = arcade.ShapeElementList()

        x_list = [face_width/2 * i for i in range(11)]
        y_list_1 = itertools.cycle([0*face_height, 1*face_height])
        y_list_2 = itertools.cycle([2*face_height, 3*face_height])
        point_list_1 = tuple(zip(x_list, y_list_1))
        point_list_2 = tuple(zip(x_list, y_list_2))

        # Borders drawing.
        border_1 = arcade.create_line_strip(point_list_1, arcade.color.WHITE, 2)
        border_2 = arcade.create_line_strip(point_list_2, arcade.color.WHITE, 2)
        self.borders.append(border_1)
        self.borders.append(border_2)

        # Cells drawing.
        cell_width = face_width / self.cells_on_edge
        cell_height = face_height / self.cells_on_edge
        for cell in self.world_map.cells:
            triangle = self._get_triangle_vertices(cell, cell_width, cell_height)
            self.dot_list.extend(triangle)

        self.update_colors()

    @staticmethod
    def _get_triangle_vertices(cell, cell_width, cell_height):
        """ Returns tuple of vertex coordinates. """
        down_y = cell.y
        up_y = cell.y + 1
        if cell.up_side_down:
            left_x = (cell.x - 1) // 2 + 0.5
        else:
            left_x = cell.x // 2
        if cell.y % 2 == 1:
            left_x -= 0.5
        middle_x = left_x + 0.5
        right_x = left_x + 1
        vertices_x = (left_x, right_x, middle_x)
        if cell.up_side_down:
            vertices_y = (up_y, up_y, down_y)
        else:
            vertices_y = (down_y, down_y, up_y)
        triangle = zip(vertices_x, vertices_y)
        triangle = list(triangle)
        for vertex_index, vertex in enumerate(tuple(triangle)):
            x, y = vertex
            vertex = (x * cell_width, y * cell_height)
            vertex = map(round, vertex)
            triangle[vertex_index] = tuple(vertex)
        return tuple(triangle)

    def update_colors(self):
        """ Map visual part update. """
        self.cells = arcade.ShapeElementList()

        color_list = []

        # Colors recalculation.
        for cell in self.world_map.cells:
            if self.mod == 'tectonic':
                color = 3 * [cell.tectonic_color]
            else:
                color = 3 * [cell.color]
            color_list.extend(color)

        cells_grid = arcade.create_triangles_filled_with_colors(self.dot_list, color_list)
        self.cells.append(cells_grid)

    def draw_player(self):
        """ Draw player. """
        # Draw circle
        player = self.player
        face_width, face_height = self.FACE_SIZE
        cell_width = face_width / self.cells_on_edge
        cell_height = face_height / self.cells_on_edge
        arcade.draw_circle_filled(round(cell_width * (player.x / 2)),
                                  round(cell_height * ((0.33 + 0.33 * (player.x % 2 == player.y % 2)) + player.y)),
                                  3,
                                  arcade.color.BLACK)
        if self.display_player_coordinates:
            # Draw numbers
            arcade.draw_text(str(player.x) + ' ' + str(player.y),
                             round(cell_width * (player.x / 2)),
                             round(cell_height * (0.33 * (player.x % 2 == player.y % 2) + player.y) + 30),
                             arcade.color.BLACK,
                             17,
                             bold=True,
                             align="center",
                             font_name=('Century Gothic', 'Arial'),
                             anchor_x="center",
                             anchor_y="center")

    def on_draw(self):
        screen_width = self.SCREEN_WIDTH
        screen_height = self.SCREEN_HEIGHT

        # Visual part render.
        arcade.start_render()

        self.cells.draw()
        self.borders.draw()
        self.draw_player()

        if self.debug_mod:
            arcade.draw_text(VERSION, 230, screen_height - 40, arcade.color.WHITE, 18,
                             font_name=('Century Gothic', 'Arial'))
            arcade.draw_text('Mod: ' + self.mod, 500, screen_height - 40, arcade.color.WHITE, 18,
                             font_name=('Century Gothic', 'Arial'))

        if self.hints_notification:
            arcade.draw_text("Press H", screen_width - 90, screen_height - 40, arcade.color.WHITE, 18,
                             font_name=('Century Gothic', 'Arial'))

        if self.hints_on:
            self.draw_hints_window()

    def on_key_press(self, symbol, modifiers: int):
        """ Input treatment. """
        # Full Screen.
        if symbol == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.set_viewport(0, self.SCREEN_WIDTH, 0, self.SCREEN_HEIGHT)

        # Debug Mod.
        if symbol == arcade.key.F3:
            self.debug_mod = not self.debug_mod

        # Common Mod.
        if symbol == arcade.key.KEY_1:
            self.mod = 'common'
            self.update_colors()

        # Tectonic Mod.
        if symbol == arcade.key.KEY_2:
            self.mod = 'tectonic'
            self.update_colors()

        # Hints.
        if symbol == arcade.key.H:
            self.hints_on = not self.hints_on
            self.hints_notification = False

        # Tectonic Generation.
        if symbol == arcade.key.T:
            self.world_map.tectonic_generation()
            if self.mod == 'tectonic':
                self.update_colors()

        # Coordinates.
        if symbol == arcade.key.S:
            self.display_player_coordinates = not self.display_player_coordinates

        # Movement.
        keys = arcade.key
        x = self.player.x
        y = self.player.y
        directions = self.world_map.get_directions(x, y)
        # TODO: remove disclosure of Icosahedron secrets
        horizontal_side_up = (x + y) % 2 == 0
        if horizontal_side_up:
            directions_by_keys = {
                (keys.Z, keys.A): directions.left,
                (keys.C, keys.D): directions.right,
                (keys.Q, keys.W, keys.E): directions.middle
            }
        else:
            directions_by_keys = {
                (keys.A, keys.Q): directions.left,
                (keys.D, keys.E): directions.right,
                (keys.Z, keys.X, keys.C): directions.middle
            }
        for key_set in directions_by_keys.keys():
            if symbol in key_set:
                direction = directions_by_keys[key_set]
                self.player.move(*direction)

    def draw_hints_window(self):
        """ Hints window drawing """
        screen_width = self.SCREEN_WIDTH
        screen_height = self.SCREEN_HEIGHT
        arcade.draw_rectangle_filled(screen_width / 2, screen_height / 2, screen_width - 200,
                                     screen_height - 200,
                                     arcade.color.BLACK)
        arcade.draw_rectangle_filled(screen_width / 2, screen_height / 2, screen_width - 204,
                                     screen_height - 204,
                                     arcade.color.WHITE)
        arcade.draw_rectangle_filled(screen_width / 2, screen_height / 2, screen_width - 208,
                                     screen_height - 208,
                                     arcade.color.BLACK)
        arcade.draw_text("Hints", screen_width / 2, screen_height / 2 + 260,
                         arcade.color.WHITE, 40, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Controls:", screen_width / 2 - 500, screen_height / 2 + 200,
                         arcade.color.WHITE, 30, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Motion:", screen_width / 2 - 480, screen_height / 2 + 100,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Q W E\nA     D\nZ  X C", screen_width / 2 - 380, screen_height / 2 + 100,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Coordinates: S", screen_width / 2 - 200, screen_height / 2 + 100,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Full Screen: F", screen_width / 2 - 450, screen_height / 2,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Hints: H", screen_width / 2 - 250, screen_height / 2,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Debug Mod: F3", screen_width / 2 - 440, screen_height / 2 - 100,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Tectonic test: T", screen_width / 2 - 440, screen_height / 2 - 200,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
