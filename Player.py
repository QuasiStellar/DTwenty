class Player(object):

    def __init__(self, x, y, world_map):
        self.x = x
        self.y = y
        self.world_map = world_map

    def move_to(self, x, y):
        """ Move player. """
        self.x = x
        self.y = y
