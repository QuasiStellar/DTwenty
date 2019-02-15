import arcade

import Game


class Player(object):

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.coord = False

    def move(self, x, y):
        self.i = (self.i + x) % (30*Game.N)
        self.j += y

    def draw(self):
        height = 260 / (Game.N * 3)
        width = 300 / (Game.N * 3)
        arcade.draw_circle_filled(round(width*(self.i/2)),
                                  round(height*((0.33+0.33*(self.i % 2 == self.j % 2))+self.j)),
                                  3,
                                  arcade.color.BLACK)
        if self.coord:
            arcade.draw_text(str(self.i)+' '+str(self.j),
                             round(width*(self.i/2)),
                             round(height*(0.33*(self.i % 2 == self.j % 2)+self.j)+30),
                             arcade.color.BLACK,
                             17,
                             bold=True,
                             align="center",
                             font_name=('Century Gothic', 'Arial'),
                             anchor_x="center",
                             anchor_y="center")
