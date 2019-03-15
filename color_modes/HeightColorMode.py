from color_modes.ColorMode import ColorMode


class HeightColorMode(ColorMode):

    def get_cell_color(self, cell):
        raise NotImplementedError("HeightColorMode.get_cell_color is not implemented")
