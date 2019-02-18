import random


class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.up_side_down = (x + y) % 2 == 0
        self.type = 0
        self.temperature = 0
        self.height = 0
        self.plate = 0

        random_color = random.randint(128, 256)
        self.color = (random_color, random_color, random_color)
