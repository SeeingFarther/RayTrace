import numpy as np


class Plane:
    def __init__(self, normal, offset, material=None):
        self.normal = normal
        self.offset = -offset
        self.material = material

    # Get and set functions
    def getNormal(self):
        return self.normal

    def getOffset(self):
        return self.offset

    def getMaterial(self):
        return self.material

    def setNormal(self, normal):
        self.normal = normal

    def setOffset(self, offset):
        self.offset = -offset

    def setMaterial(self, material):
        self.material = material

    # Calculate intersection between the ray and the plane using algebraic method
    def findIntersection(self, P_0, vector):
        div = np.dot(vector, self.normal)
        prod = np.dot(self.normal, P_0) + self.offset
        if div == 0:
            return np.inf * -prod

        t = -prod / div
        return t

    # Get and set functions
    def getNormal(self, ray=None):
        return self.normal
