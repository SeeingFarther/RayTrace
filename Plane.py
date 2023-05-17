import numpy as np


class Plane:
    def __init__(self, normal, offset, material):
        self.normal = normal
        self.offset = offset
        self.material = material

    # Calculate intersection between the ray and the plane using algebraic method
    def intersect(self, P_0, vector):
        div = vector.dot(self.normal)
        prod = P_0.dot(self.normal) + self.offset
        t = -prod / div
        return t

    # Get the plane normal
    def getNormal(self):
        return self.normal

    # Find vector projection on plane
    def findProjection(self, vector):
        projection = vector - self.normal * vector.dot(self.normal)
        return projection
