import numpy as np


class Plane:
    def __init__(self, normal, offset, material):
        self.normal = normal
        self.offset = offset
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
        self.offset = offset

    def setMaterial(self, material):
        self.material = material

    # Calculate intersection between the ray and the plane using algebraic method
    def intersect(self, P_0, vector):
        div = vector.dot(self.normal)
        prod = P_0.dot(self.normal) + self.offset
        t = -prod / div
        return t

    # Find vector projection on plane
    def findProjection(self, vector):
        projection = vector - self.normal * vector.dot(self.normal)
        return projection
