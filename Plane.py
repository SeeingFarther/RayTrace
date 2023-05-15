import numpy as np

class Plane:
    def __init__(self, normal, offset, material):
        self.normal = normal
        self.offset = offset
        self.material = material

    # Calculate intersection between the ray and the plane using algebraic method
    def intersect(self, P_0, V):
        div = V.dot(self.normal)
        prod = P_0.dot(self.normal) + self.offset
        t = -prod / div
        return t