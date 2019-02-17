import random

import Game


class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.up_side_down = (x + y) % 2 == 0
        self.exist = True
        self.type = 0
        self.temperature = 0
        self.height = 0

        random_color = random.randint(128, 256)
        self.color = (random_color, random_color, random_color)

        if y < 3*Game.N:
            xx = x % (6 * Game.N)
            if xx <= 3*Game.N:
                if xx > y:
                    self.exist = False
            else:
                if 6*Game.N-xx > y:
                    self.exist = False
        elif y >= 6*Game.N:
            xx = x % (6 * Game.N)
            yy = y % (6 * Game.N)
            if xx <= 3*Game.N:
                if xx <= yy:
                    self.exist = False
            else:
                if 6*Game.N-xx <= yy:
                    self.exist = False

    @staticmethod
    def near(x, y):
        xx = x % (6 * Game.N)
        yy = y % (6 * Game.N)
        if (x + y) % 2 == 0:
            if y == 0:
                return [(-6*Game.N, 0),
                        (0, 0),
                        (6*Game.N, 0),
                        (-6*Game.N, 0),
                        (6*Game.N, 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            if xx == yy and y < 3*Game.N:
                return [(-1, 0),
                        (0, 0),
                        (2*(3*Game.N-yy), 0),
                        (-1, 0),
                        (2*(3*Game.N-yy), 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            if (6*Game.N - xx) == yy and y < 3*Game.N:
                return [(-2*(3*Game.N-yy), 0),
                        (0, 0),
                        (1, 0),
                        (-2*(3*Game.N-yy), 0),
                        (1, 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            return [(-1, 0), (0, 0), (1, 0), (-1, 0), (1, 0), (0, 1), (0, 1), (0, 1)]
        else:
            if y == 9*Game.N-1:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-6*Game.N, 0),
                        (6*Game.N, 0),
                        (-6*Game.N, 0),
                        (0, 0),
                        (6*Game.N, 0)]
            if xx-1 == yy and y >= 6*Game.N:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-2*(yy+1), 0),
                        (1, 0),
                        (-2*(yy+1), 0),
                        (0, 0),
                        (1, 0)]
            if (6*Game.N - xx - 1) == yy and y >= 6*Game.N:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-1, 0),
                        (2*(yy+1), 0),
                        (-1, 0),
                        (0, 0),
                        (2*(yy+1), 0)]
            return [(0, -1), (0, -1), (0, -1), (-1, 0), (1, 0), (-1, 0), (0, 0), (1, 0)]
