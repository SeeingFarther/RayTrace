import numpy as np
from Plane import *

class Triangle:
    def __init__(self, T1, T2, T3):
        self.T1 = T1
        self.T2 = T2
        self.T3 = T3

        # Finds normal
        v = T2 - T1
        u = T3 - T1
        self.normal = np.cross(v, u)
        self.normal = self.normal / np.linalg.norm(self.normal)

        # Finds offset
        offset = np.dot(T1, self.normal)
        self.triangle_plane = Plane(self.normal, offset)

    # Get normal
    def getNormal(self, ray=None):
        return self.normal

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

        # Checks if in triangle for each two points of the triangle
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


