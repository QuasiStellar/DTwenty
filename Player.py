import Game


class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """ Move player. """
        self.x = (self.x + dx) % (30 * Game.N)
        self.y += dy
