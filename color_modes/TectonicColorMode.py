from color_modes.ColorMode import ColorMode


class TectonicColorMode(ColorMode):

    def get_cell_color(self, cell):
        min_color = 100
        max_color = 255
        max_plate_index = self.world_map.tectonic_plates_count - 1
        k = cell.plate.index / max_plate_index
        color = min_color + k * (max_color - min_color)
        return (int(color),) * 3

    def can_be_enabled(self):
        if not self.world_map.tectonic_plates_generated:
            return False
        return super().can_be_enabled()
