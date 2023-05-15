import numpy as np


class Camera:
    def __init__(self, position, V_to, V_up, screen_distance, screen_width, use_fisheye, fisheye_k):
        self.position = position
        self.V_to = V_to
        self.V_up = V_up
        self.screen_distance = screen_distance
        self.screen_width = screen_width
        self.use_fisheye = use_fisheye
        self.fisheye_k = fisheye_k
