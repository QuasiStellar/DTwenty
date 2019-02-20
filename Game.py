import arcade
import os
import timeit

import Player
import WorldMap

VERSION = "alpha-0.2"

""" Path for files (not used yet). """
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

""" Size of the default window. """
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 780

SCREEN_TITLE = "D20"

""" Amount of plates into which we divide the map. """
TECTONIC_PLATES = 5

N = 2
""" You can change this constant. It determines an amount of cells on your map (3N cells on one side).
    Remember that quantity is proportional to the square of edge length.
    Huge values can cause lags and Memory Error (N>80) """

""" WorldMap object - main map. """
world_map = WorldMap.WorldMap(N)


class Game(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, SCREEN_TITLE, fullscreen=False)

        # Player object - a dot moving through the map.
        self.player = Player.Player(0, 0)

        # ShapeElementList object for borders drawing. See setup()
        self.borders = None

        # ShapeElementList object for cells drawing. See setup() & re_setup()
        self.cells = None

        # Time tracking.
        self.draw_time = 0

        self.hints_on = False
        self.hints_notification = True
        self.debug_mod = False

        # List of dots for drawing.
        self.dot_list = []

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Map visual part setup."""
        self.borders = arcade.ShapeElementList()

        # Coordinates for default window size.
        point_list_1 = ((0, 520),
                        (150, 780),
                        (300, 520),
                        (450, 780),
                        (600, 520),
                        (750, 780),
                        (900, 520),
                        (1050, 780),
                        (1200, 520),
                        (1350, 780),
                        (1500, 520))
        point_list_2 = ((1500, 0),
                        (1350, 260),
                        (1200, 0),
                        (1050, 260),
                        (900, 0),
                        (750, 260),
                        (600, 0),
                        (450, 260),
                        (300, 0),
                        (150, 260),
                        (0, 0))

        # Borders drawing.
        border_1 = arcade.create_line_strip(point_list_1, arcade.color.WHITE, 2)
        border_2 = arcade.create_line_strip(point_list_2, arcade.color.WHITE, 2)
        self.borders.append(border_1)
        self.borders.append(border_2)

        # Cells drawing.
        self.cells = arcade.ShapeElementList()
        color_list = []

        cell_height = 260 / (N * 3)
        cell_width = 300 / (N * 3)

        for cell in world_map.cells:
            triangle = self._get_triangle_vertices(cell, cell_width, cell_height)
            for vertex in triangle:
                self.dot_list.append(vertex)
            color_list.extend(3*[cell.color])

        cells_grid = arcade.create_triangles_filled_with_colors(self.dot_list, color_list)
        self.cells.append(cells_grid)

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

    def re_setup(self):
        """ Map visual part update. """
        self.cells = arcade.ShapeElementList()

        color_list = []

        # Colors recalculation.
        for cell in world_map.cells:
            color = 3*[cell.color]
            color_list.extend(color)

        cells_grid = arcade.create_triangles_filled_with_colors(self.dot_list, color_list)
        self.cells.append(cells_grid)

    def on_draw(self):
        # Visual part render.
        arcade.start_render()
        # Timer zeroing.
        draw_start_time = timeit.default_timer()

        self.cells.draw()
        self.borders.draw()
        self.player.draw()

        if self.debug_mod:
            output = f"{1/(self.draw_time+0.001):.0f} fps"
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 18,
                             font_name=('Century Gothic', 'Arial'))
            arcade.draw_text(VERSION, 230, SCREEN_HEIGHT - 40, arcade.color.WHITE, 18,
                             font_name=('Century Gothic', 'Arial'))

        if self.hints_notification:
            arcade.draw_text("Press H", SCREEN_WIDTH - 90, SCREEN_HEIGHT - 40, arcade.color.WHITE, 18,
                             font_name=('Century Gothic', 'Arial'))

        if self.hints_on:
            self.draw_hints_window()

        self.draw_time = timeit.default_timer() - draw_start_time

    def update(self, delta_time):
        pass

    def on_key_press(self, symbol, modifiers: int):
        """ Input treatment. """
        # Full Screen.
        if symbol == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        # Debug Mod.
        if symbol == arcade.key.F3:
            self.debug_mod = not self.debug_mod

        # Hints.
        if symbol == arcade.key.H:
            self.hints_on = not self.hints_on
            self.hints_notification = False

        # Tectonic Generation (WIP).
        if symbol == arcade.key.T:
            world_map.tectonic(TECTONIC_PLATES)
            self.re_setup()

        # Coordinates.
        if symbol == arcade.key.S:
            self.player.coord = not self.player.coord

        # Movement.
        movement_keys = (
            arcade.key.Z,
            arcade.key.X,
            arcade.key.C,
            arcade.key.A,
            arcade.key.D,
            arcade.key.Q,
            arcade.key.W,
            arcade.key.E
        )
        if symbol in movement_keys:
            x = self.player.x
            y = self.player.y
            direction_index = movement_keys.index(symbol)
            direction = world_map.get_directions(x, y)[direction_index]
            self.player.move(*direction)

    @staticmethod
    def draw_hints_window():
        """ Hints window drawing """
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH - 200,
                                     SCREEN_HEIGHT - 200,
                                     arcade.color.BLACK)
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH - 204,
                                     SCREEN_HEIGHT - 204,
                                     arcade.color.WHITE)
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH - 208,
                                     SCREEN_HEIGHT - 208,
                                     arcade.color.BLACK)
        arcade.draw_text("Hints", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 260,
                         arcade.color.WHITE, 40, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Controls:", SCREEN_WIDTH / 2 - 500, SCREEN_HEIGHT / 2 + 200,
                         arcade.color.WHITE, 30, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Motion:", SCREEN_WIDTH / 2 - 480, SCREEN_HEIGHT / 2 + 100,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Q W E\nA     D\nZ  X C", SCREEN_WIDTH / 2 - 380, SCREEN_HEIGHT / 2 + 100,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Coordinates: S", SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 100,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Full Screen: F", SCREEN_WIDTH / 2 - 450, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Hints: H", SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Debug Mod: F3", SCREEN_WIDTH / 2 - 440, SCREEN_HEIGHT / 2 - 100,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")
        arcade.draw_text("Tectonic test: T", SCREEN_WIDTH / 2 - 440, SCREEN_HEIGHT / 2 - 200,
                         arcade.color.WHITE, 20, width=200, bold=True,
                         align="center", font_name=('Century Gothic', 'Arial'), anchor_x="center", anchor_y="center")


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
