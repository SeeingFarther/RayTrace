import numpy as np
from utilities import normalize

class Sphere:
    def __init__(self, position, radius, material_index):
        self.position = position
        self.radius = radius
        self.material_index = material_index

    # Get and set functions
    def getPosition(self):
        return self.position

    def getRadius(self):
        return self.radius

    def getMaterial(self):
        return self.material_index

    def setPosition(self, position):
        self.position = position

    def setRadius(self, radius):
        self.radius = radius

    def setMaterial(self, material_index):
        self.material_index = material_index

    # Calculate intersection between the ray and the sphere using geometric method we learnt in the lecture
    def findIntersection(self, P_0, V):
        # Calculate L and T_ca
        L = self.position - P_0
        T_ca = np.dot(L, V)
        if T_ca < 0:
            return 0

        # Calculate d^2
        d_squared = L.dot(L) - (T_ca * T_ca)
        if d_squared > self.radius * self.radius:
            return 0

        # Calculate T_hc
        T_hc = np.sqrt(self.radius * self.radius - d_squared)
        t1 = T_ca - T_hc
        t2 = T_ca + T_hc

        # Checks for the closet positive from the two intersection points else return zero
        if t1 <= 0 and t2 <= 0:
            return 0

        if t1 > t2:
            t1, t2 = t2, t1

        if t1 < 0:
            t1 = t2
        return t1

    # Gives the normal of point on the sphere
    def getNormal(self, ray):
        V = ray.getIntersectionPoint()
        normal = V - self.position
        return normalize(normal)
