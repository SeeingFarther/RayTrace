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
        L = self.position - P_0
        t_ca = np.dot(L, V)

        if t_ca < 0:
            return 0

        dSquare = np.dot(L, L) - np.power(t_ca, 2)

        if dSquare > np.power(self.radius, 2):
            return 0

        t_hc = np.sqrt(np.power(self.radius, 2) - dSquare)
        t = min(t_ca - t_hc, t_ca + t_hc)

        return t

    # Gives the normal of point on the sphere
    def getNormal(self, ray):
        V = ray.getIntersectionPoint()
        normal = V - self.position
        return normalize(normal)
