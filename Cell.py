import random

import Game
import WorldMap


class Cell(object):

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.up_side_down = (i + j) % 2 == 0
        self.exist = True
        self.type = 0
        self.temperature = 0
        self.height = 0
        self.plate = None

        random_color = random.randint(128, 256)
        self.color = (random_color, random_color, random_color)

        if j < 3*Game.N:
            ii = i % (6 * Game.N)
            if ii <= 3 * Game.N:
                if ii > j:
                    self.exist = False
            else:
                if 6 * Game.N - ii > j:
                    self.exist = False
        elif j >= 6 * Game.N:
            ii = i % (6 * Game.N)
            jj = j % (6 * Game.N)
            if ii <= 3 * Game.N:
                if ii <= jj:
                    self.exist = False
            else:
                if 6 * Game.N-ii <= jj:
                    self.exist = False

    @staticmethod
    def random_cell():
        while True:
            i = random.randint(0, 30 * Game.N - 1)
            j = random.randint(0, 9 * Game.N - 1)
            if Game.world_map.map[i][j].exist:
                random_cell = (i, j)
                return random_cell

    @staticmethod
    def near(i, j):
        ii = i % (6 * Game.N)
        jj = j % (6 * Game.N)
        if (i+j) % 2 == 0:
            if j == 0:
                return [(-6 * Game.N, 0),
                        (0, 0),
                        (6 * Game.N, 0),
                        (-6 * Game.N, 0),
                        (6 * Game.N, 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            if ii == jj and j < 3 * Game.N:
                return [(-1, 0),
                        (0, 0),
                        (2 * (3 * Game.N - jj), 0),
                        (-1, 0),
                        (2 * (3 * Game.N - jj), 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            if (6 * Game.N - ii) == jj and j < 3 * Game.N:
                return [(-2 * (3 * Game.N - jj), 0),
                        (0, 0),
                        (1, 0),
                        (-2 * (3 * Game.N - jj), 0),
                        (1, 0),
                        (0, 1),
                        (0, 1),
                        (0, 1)]
            return [(-1, 0), (0, 0), (1, 0), (-1, 0), (1, 0), (0, 1), (0, 1), (0, 1)]
        else:
            if j == 9 * Game.N - 1:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-6 * Game.N, 0),
                        (6 * Game.N, 0),
                        (-6 * Game.N, 0),
                        (0, 0),
                        (6 * Game.N, 0)]
            if ii - 1 == jj and j >= 6 * Game.N:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-2 * (jj + 1), 0),
                        (1, 0),
                        (-2 * (jj + 1), 0),
                        (0, 0),
                        (1, 0)]
            if (6 * Game.N - ii - 1) == jj and j >= 6 * Game.N:
                return [(0, -1),
                        (0, -1),
                        (0, -1),
                        (-1, 0),
                        (2 * (jj + 1), 0),
                        (-1, 0),
                        (0, 0),
                        (2 * (jj + 1), 0)]
            return [(0, -1), (0, -1), (0, -1), (-1, 0), (1, 0), (-1, 0), (0, 0), (1, 0)]
