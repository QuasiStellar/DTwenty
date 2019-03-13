import arcade

from WorldMapWidget import WorldMapWidget

import Player
import world_map.WorldMap as WorldMap

VERSION = "alpha-0.3"
SCREEN_TITLE = "D20"


class Game(arcade.Window):

    def __init__(self, n, tectonic_plates_count, submergence, seed):
        # Size of the default window.
        self.screen_size_px = (1500, 780)

        screen_width, screen_height = self.screen_size_px
        super().__init__(screen_width, screen_height, SCREEN_TITLE, fullscreen=False)

        # WorldMap object - main map
        self.world_map = WorldMap.WorldMap(n, tectonic_plates_count, submergence, seed)
        self._world_map_widget = WorldMapWidget(
            world_map=self.world_map,
            size_px=self.screen_size_px
        )

        # Player object - a dot moving through the map
        self.player = Player.Player(cell=self.world_map[0, 0], world_map=self.world_map)

        self.hints_on = False
        self.hints_notification = True
        self.debug_mode = False
        self.display_player_coordinates = None

        arcade.set_background_color(arcade.color.BLACK)

    def _draw_player(self):
        """ Draw player. """
        cell_width, cell_height = self._world_map_widget.cell_size_px
        cell = self.player.cell
        x = (cell.pos.x / 2) * cell_width
        y = cell.pos.y * cell_height
        cell_upside_down = self.world_map.is_upside_down(cell)
        if cell_upside_down:
            y += 0.33*cell_height
        # Draw circle
        arcade.draw_circle_filled(round(x),
                                  round(y + 0.33*cell_height),
                                  radius=3,
                                  color=arcade.color.BLACK)
        if self.display_player_coordinates:
            # Draw numbers
            arcade.draw_text("%s %s" % cell.pos,
                             round(x),
                             round(y + 30),
                             color=arcade.color.BLACK,
                             font_size=17,
                             bold=True,
                             align="center",
                             font_name=('Century Gothic', 'Arial'),
                             anchor_x="center",
                             anchor_y="center")

    def on_draw(self):
        screen_width, screen_height = self.screen_size_px

        # Visual part render
        arcade.start_render()

        self._world_map_widget.on_draw()
        self._draw_player()

        if self.debug_mode:
            arcade.draw_text(VERSION,
                             230, screen_height - 40,
                             color=arcade.color.WHITE,
                             font_size=18,
                             font_name=('Century Gothic', 'Arial'))
            arcade.draw_text('Mode: ' + self._world_map_widget.color_mode,
                             500, screen_height - 40,
                             color=arcade.color.WHITE,
                             font_size=18,
                             font_name=('Century Gothic', 'Arial'))

        if self.hints_notification:
            arcade.draw_text("Press H",
                             screen_width - 90, screen_height - 40,
                             color=arcade.color.WHITE,
                             font_size=18,
                             font_name=('Century Gothic', 'Arial'))

        if self.hints_on:
            self._draw_hints_window()

    def on_key_press(self, symbol, modifiers: int):
        """ Input treatment. """
        # Full Screen
        if symbol == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            screen_width, screen_height = self.screen_size_px
            self.set_viewport(0, screen_width, 0, screen_height)

        # Debug Mode
        if symbol == arcade.key.F3:
            self.debug_mode = not self.debug_mode

        # Hints
        if symbol == arcade.key.H:
            self.hints_on = not self.hints_on
            self.hints_notification = False

        # Display Player Coordinates ON/OFF
        if symbol == arcade.key.S:
            self.display_player_coordinates = not self.display_player_coordinates

        # Common Mode
        if symbol == arcade.key.KEY_1:
            self._world_map_widget.set_color_mode("common")

        # Tectonic Mode
        if symbol == arcade.key.KEY_2 and self.world_map.tectonic_plates_generated:
            self._world_map_widget.set_color_mode("tectonic")

        # Tectonic Generation
        if symbol == arcade.key.T and not self.world_map.tectonic_plates_generated:
            self.world_map.tectonic_generation()

        # Movement
        keys = arcade.key
        cell = self.player.cell
        neighbors = self.world_map.get_cells_near(cell)
        cell_upside_down = self.world_map.is_upside_down(cell)
        if cell_upside_down:
            neighbors_by_keys = {
                (keys.Z, keys.A): neighbors.left,
                (keys.C, keys.D): neighbors.right,
                (keys.Q, keys.W, keys.E): neighbors.middle
            }
        else:
            neighbors_by_keys = {
                (keys.A, keys.Q): neighbors.left,
                (keys.D, keys.E): neighbors.right,
                (keys.Z, keys.X, keys.C): neighbors.middle
            }
        for key_set in neighbors_by_keys.keys():
            if symbol in key_set:
                neighbor = neighbors_by_keys[key_set]
                self.player.move_to(neighbor)

    def _draw_hints_window(self):
        """ Hints window drawing """
        screen_width, screen_height = self.screen_size_px

        arcade.draw_rectangle_filled(screen_width / 2, screen_height / 2,
                                     screen_width - 200, screen_height - 200,
                                     arcade.color.BLACK)
        arcade.draw_rectangle_filled(screen_width / 2, screen_height / 2,
                                     screen_width - 204, screen_height - 204,
                                     arcade.color.WHITE)
        arcade.draw_rectangle_filled(screen_width / 2, screen_height / 2,
                                     screen_width - 208, screen_height - 208,
                                     arcade.color.BLACK)

        def draw_text(*args, **kwargs):
            default_kwargs = dict(
                color=arcade.color.WHITE,
                width=200,
                bold=True,
                align="center",
                font_name=('Century Gothic', 'Arial'),
                anchor_x="center",
                anchor_y="center"
            )
            for key, value in default_kwargs.items():
                if key not in kwargs:
                    kwargs[key] = value
            arcade.draw_text(*args, **kwargs)

        draw_text("Hints",
                  screen_width / 2,
                  screen_height / 2 + 260,
                  font_size=40)
        draw_text("Controls:",
                  screen_width / 2 - 500,
                  screen_height / 2 + 200,
                  font_size=30)
        draw_text("Motion:",
                  screen_width / 2 - 480,
                  screen_height / 2 + 100,
                  font_size=20)
        draw_text("Q W E\nA     D\nZ  X C",
                  screen_width / 2 - 380,
                  screen_height / 2 + 100,
                  font_size=20)
        draw_text("Coordinates: S",
                  screen_width / 2 - 200,
                  screen_height / 2 + 100,
                  font_size=20)
        draw_text("Full Screen: F",
                  screen_width / 2 - 450,
                  screen_height / 2,
                  font_size=20)
        draw_text("Hints: H",
                  screen_width / 2 - 250,
                  screen_height / 2,
                  font_size=20)
        draw_text("Debug Mod: F3",
                  screen_width / 2 - 440,
                  screen_height / 2 - 100,
                  font_size=20)
        draw_text("Tectonic test: T",
                  screen_width / 2 - 440,
                  screen_height / 2 - 200,
                  font_size=20)
