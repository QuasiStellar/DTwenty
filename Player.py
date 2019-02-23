import arcade

import Game


class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.display_coordinates = False

    def move(self, dx, dy):
        """ Move player. """
        self.x = (self.x + dx) % (30 * Game.N)
        self.y += dy

    def draw(self):
        """ Draw player. """
        # Draw circle
        edge_size = 3*Game.N
        face_width, face_height = Game.FACE_SIZE
        cell_width = face_width / edge_size
        cell_height = face_height / edge_size
        arcade.draw_circle_filled(round(cell_width * (self.x / 2)),
                                  round(cell_height * ((0.33 + 0.33 * (self.x % 2 == self.y % 2)) + self.y)),
                                  3,
                                  arcade.color.BLACK)
        if self.display_coordinates:
            # Draw numbers
            arcade.draw_text(str(self.x) + ' ' + str(self.y),
                             round(cell_width * (self.x / 2)),
                             round(cell_height * (0.33 * (self.x % 2 == self.y % 2) + self.y) + 30),
                             arcade.color.BLACK,
                             17,
                             bold=True,
                             align="center",
                             font_name=('Century Gothic', 'Arial'),
                             anchor_x="center",
                             anchor_y="center")
