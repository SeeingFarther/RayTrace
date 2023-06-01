import numpy as np
from .infinite_plane import InfinitePlane


class Triangle:
    def __init__(self, T1, T2, T3, material_index):
        self.T1 = T1
        self.T2 = T2
        self.T3 = T3
        self.material_index = material_index

        # Finds normal
        v = T2 - T1
        u = T3 - T1
        self.normal = np.cross(v, u)
        self.normal = self.normal / np.linalg.norm(self.normal)

        # Finds offset
        offset = np.dot(T1, self.normal)
        self.triangle_plane = InfinitePlane(self.normal, -offset, material_index)

    # Get and set functions
    def getT1(self):
        return self.T1

    def getT2(self):
        return self.T2

    def getT3(self):
        return self.T3

    def getMaterial(self):
        return self.material_index

    def setT1(self, T1):
        self.T1 = T1

    def setT2(self, T2):
        self.T2 = T2

    def setT3(self, T3):
        self.T3 = T3

    def setMaterial(self, material_index):
        self.material_index = material_index

    def getNormal(self, ray=None):
        return self.normal

    # Check if inside the plane defined by two vectors
    def checkInside(self, V1, V2, P_0, P):
        # Finds normal
        N = np.cross(V1, V2)
        N = N / np.linalg.norm(N)

        # Finds offset
        offset = -np.dot(N, P_0)

        if np.dot(P, N) + offset < 0:
            return np.inf

    # Check if point is inside triangle algebraically like learned in the lecture
    def findIntersection(self, P_0, V):
        t = self.triangle_plane.findIntersection(P_0, V)
        P = P_0 + t * V

        # Checks if in plane defined by each two points of the triangle? if yes return inside the triangle
        V1 = self.T1 - P_0
        V2 = self.T2 - P_0
        if self.checkInside(V1, V2, P_0, P) == np.inf:
            return np.inf

        V1 = self.T1 - P_0
        V2 = self.T3 - P_0
        if self.checkInside(V1, V2, P_0, P) == np.inf:
            return np.inf

        V1 = self.T2 - P_0
        V2 = self.T3 - P_0
        if self.checkInside(V1, V2, P_0, P) == np.inf:
            return np.inf

        return t