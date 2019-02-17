import arcade
import os
import timeit

import Player
import Cell
import WorldMap

VERSION = "alpha-0.2"

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 780

SCREEN_TITLE = "D20"

N = 8
""" You can change this constant. It determines an amount of cells on your map (3N cells on one side).
    Remember that quantity is proportional to the square of edge length.
    Huge values can cause lags and Memory Error (N>80) """

world_map = WorldMap.WorldMap()


class Game(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, SCREEN_TITLE, fullscreen=False)

        self.player = Player.Player(0, 0)
        self.borders = None
        self.cells = None
        self.draw_time = 0
        self.hints_on = False
        self.hints_notification = True

        self.cell_list = []

        self.debug_mod = False

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.borders = arcade.ShapeElementList()
        self.cells = arcade.ShapeElementList()

        color_list = []

        height = 260 / (N * 3)
        width = 300 / (N * 3)

        for horizontal in world_map.map:
            for cell in horizontal:
                if cell.exist:
                    if cell.up_side_down:
                        left_up = (round(((cell.i - 1) // 2 + 0.5) * width) - round(width * 0.5 * (cell.j % 2 == 1)),
                                   round((cell.j + 1) * height))
                        right_up = (round(((cell.i - 1) // 2 + 1.5) * width) - round(width * 0.5 * (cell.j % 2 == 1)),
                                    round((cell.j + 1) * height))
                        bottom = (round(((cell.i - 1) // 2 + 1) * width) - round(width * 0.5 * (cell.j % 2 == 1)),
                                  round(cell.j * height))
                        self.cell_list.append(left_up)
                        self.cell_list.append(right_up)
                        self.cell_list.append(bottom)
                        for i in range(3):
                            color_list.append(cell.color)
                    else:
                        left_down = (round(cell.i // 2 * width) - round(0.5 * width * (cell.j % 2 == 1)),
                                     round(cell.j * height))
                        right_down = (round((cell.i // 2 + 1) * width) - round(0.5 * width * (cell.j % 2 == 1)),
                                      round(cell.j * height))
                        top = (round((cell.i // 2 + 0.5) * width) - round(0.5 * width * (cell.j % 2 == 1)),
                               round((cell.j + 1) * height))
                        self.cell_list.append(left_down)
                        self.cell_list.append(right_down)
                        self.cell_list.append(top)
                        for i in range(3):
                            color_list.append(cell.color)

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

        border_1 = arcade.create_line_strip(point_list_1, arcade.color.WHITE, 2)
        border_2 = arcade.create_line_strip(point_list_2, arcade.color.WHITE, 2)
        cells_grid = arcade.create_triangles_filled_with_colors(self.cell_list, color_list)

        self.borders.append(border_1)
        self.borders.append(border_2)
        self.cells.append(cells_grid)

    def re_setup(self):
        self.cells = arcade.ShapeElementList()

        color_list = []

        for horizontal in world_map.map:
            for cell in horizontal:
                if cell.exist:
                    for i in range(3):
                        color_list.append(cell.color)

        cells_grid = arcade.create_triangles_filled_with_colors(self.cell_list, color_list)

        self.cells.append(cells_grid)

    def on_draw(self):

        arcade.start_render()

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
        if symbol == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        if symbol == arcade.key.F3:
            self.debug_mod = not self.debug_mod

        if symbol == arcade.key.H:
            self.hints_on = not self.hints_on
            self.hints_notification = False

        if symbol == arcade.key.T:
            world_map.tectonic(5)
            self.re_setup()

        i = self.player.i
        j = self.player.j
        if symbol == arcade.key.Z:
            self.player.move(Cell.Cell.near(i, j)[0][0], Cell.Cell.near(i, j)[0][1])
        if symbol == arcade.key.X:
            self.player.move(Cell.Cell.near(i, j)[1][0], Cell.Cell.near(i, j)[1][1])
        if symbol == arcade.key.C:
            self.player.move(Cell.Cell.near(i, j)[2][0], Cell.Cell.near(i, j)[2][1])
        if symbol == arcade.key.A:
            self.player.move(Cell.Cell.near(i, j)[3][0], Cell.Cell.near(i, j)[3][1])
        if symbol == arcade.key.S:
            self.player.coord = not self.player.coord
        if symbol == arcade.key.D:
            self.player.move(Cell.Cell.near(i, j)[4][0], Cell.Cell.near(i, j)[4][1])
        if symbol == arcade.key.Q:
            self.player.move(Cell.Cell.near(i, j)[5][0], Cell.Cell.near(i, j)[5][1])
        if symbol == arcade.key.W:
            self.player.move(Cell.Cell.near(i, j)[6][0], Cell.Cell.near(i, j)[6][1])
        if symbol == arcade.key.E:
            self.player.move(Cell.Cell.near(i, j)[7][0], Cell.Cell.near(i, j)[7][1])

    def tectonic_generation(self):
        pass

    @staticmethod
    def draw_hints_window():
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