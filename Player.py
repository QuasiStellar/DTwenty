class Player(object):

    def __init__(self, x, y, world_map):
        self.x = x
        self.y = y
        self.world_map = world_map

    def move(self, dx, dy):
        """ Move player. """
        self.x = (self.x + dx) % self.world_map.size.x
        self.y += dy
