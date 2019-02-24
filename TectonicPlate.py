class TectonicPlate(object):

    def __init__(self, number):
        self.number = number
        self.direction = None
        self.velocity = None
        self.cells = set()
        self.overgrowth_factor = 1
        self.size = 0
