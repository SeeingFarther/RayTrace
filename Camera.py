import numpy as np


class Camera:
    def __init__(self, position, lookTo, up, screen_distance, screen_width, use_fisheye, fisheye_k):
        self.position = position
        self.lookTo = lookTo
        self.up = up
        self.screen_distance = screen_distance
        self.screen_width = screen_width
        self.use_fisheye = use_fisheye
        self.fisheye_k = fisheye_k

    # Get and set functions
    def getPosition(self):
        return self.position

    def getLookTo(self):
        return self.lookTo

    def getUp(self):
        return self.up

    def getScreenDistance(self):
        return self.screen_distance

    def getScreenWidth(self):
        return self.screen_width

    def getUseFisheye(self):
        return self.use_fisheye

    def getFisheyeK(self):
        return self.fisheye_k

    def setPosition(self, position):
        self.position = position

    def setLookTo(self,lookTo):
        self.lookTo = lookTo

    def setUp(self, up):
        self.up = up

    def setScreenDistance(self, screen_distance):
        self.screen_distance = screen_distance

    def setScreenWidth(self, screen_width):
        self.screen_width = screen_width

    def setUseFisheye(self, use_fisheye):
        self.use_fisheye = use_fisheye

    def setFisheyeK(self, fisheye_k):
        self.fisheye_k = fisheye_k