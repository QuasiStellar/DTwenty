from abc import ABCMeta, abstractmethod


class ColorMode(metaclass=ABCMeta):
    def __init__(self, *, world_map):
        self.world_map = world_map

    @abstractmethod
    def get_cell_color(self, cell):
        pass

    def can_be_enabled(self):
        return True
