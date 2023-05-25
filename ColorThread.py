from threading import Thread
from ColorFinder import *


class ColorThread(Thread):

    # Override the constructor
    def __init__(self, ray, row, col, rgb_data, color_finder, material, surface, max_rec):
        # Init thread class constructor
        super().__init__()

        # Store fields
        self.ray = ray
        self.row = row
        self.col = col
        self.rgb_data = rgb_data
        self.color_finder = color_finder
        self.material = material
        self.surface = surface
        self.max_rec = max_rec

    # Override the run function
    def run(self):
        # Find color
        color = self.color_finder.calculateColor(self.ray, self.material, self.surface, self.max_rec)
        self.rgb_data[self.row, self.col, :] = color * 255
