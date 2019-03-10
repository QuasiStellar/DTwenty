class Player(object):

    def __init__(self, cell, world_map):
        self.cell = cell
        self.world_map = world_map

    def move_to(self, cell):
        """ Move player. """
        self.cell = cell
