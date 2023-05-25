from Plane import *
import numpy as np


class Box:
    def __init__(self, position, scale, material=None):
        self.position = position
        self.scale = scale
        self.material = material

        # Initialize min max points
        half_distance = scale * 0.5
        self.min_x = position[0] - half_distance
        self.max_x = position[0] + half_distance
        self.min_y = position[1] - half_distance
        self.max_y = position[1] + half_distance
        self.min_z = position[2] - half_distance
        self.max_z = position[2] + half_distance

        # Initialize planes for slabs method
        self.planes = [
            Plane(np.array([1, 0, 0]), self.max_x, material)
            , Plane(np.array([1, 0, 0]), self.min_x, material)
            , Plane(np.array([0, 1, 0]), self.max_y, material)
            , Plane(np.array([0, 1, 0]), self.min_y, material)
            , Plane(np.array([0, 0, 1]), self.max_z, material)
            , Plane(np.array([0, 0, 1]), self.min_z, material)]

    # Get and set functions
    def getPosition(self):
        return self.position

    def getScale(self):
        return self.scale

    def getMaterial(self):
        return self.material

    def setPosition(self, position):
        self.position = position

    def setScale(self, scale):
        self.scale = scale

    def setMaterial(self, material):
        self.material = material

    # Calculate using the slab method
    # https://www.cs.cornell.edu/courses/cs4620/2013fa/lectures/03raytracing1.pdf
    def findIntersection(self, P_0, V):
        t_entry = -np.inf
        t_exit = np.inf

        for i in range(0, len(self.planes), 2):
            # Reverse planes? (depends on direction of ray)
            index = int(np.floor(np.sqrt(i)))
            entry_plane = self.planes[i + 1] if V[index] >= 0 else self.planes[i]
            exit_plane = self.planes[i] if V[index] >= 0 else self.planes[i + 1]

            # Find the intersection points
            t_entry_plane = entry_plane.findIntersection(P_0, V)
            t_exit_plane = exit_plane.findIntersection(P_0, V)

            # Did we find min intersection points?
            if t_entry_plane > t_entry:
                t_entry = t_entry_plane
            if t_exit_plane < t_exit:
                t_exit = t_exit_plane

        # Valid intersections point?
        if t_entry == -np.inf or t_exit == np.inf:
            return -1

        if t_entry > t_exit:
            return -1

        return t_entry

    def getNormal(self, ray):
        t_entry = np.inf
        normal = np.array([0, 0, 0])
        p = ray.getP()
        ray_direction = ray.getDirection()
        for plane in self.planes:
            t = plane.findIntersection(p, ray_direction)
            if t_entry > t > 0:
                t_entry = t
                normal = plane.getNormal()

        return normal
