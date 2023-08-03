from .infinite_plane import InfinitePlane
from utilities import normalize
import numpy as np


class Cube:
    def __init__(self, position, scale, material_index):
        self.position = position
        self.scale = scale
        self.material_index = material_index

        # Initialize min max points
        half_distance = scale * 0.5
        min_x = position[0] - half_distance
        max_x = position[0] + half_distance
        min_y = position[1] - half_distance
        max_y = position[1] + half_distance
        min_z = position[2] - half_distance
        max_z = position[2] + half_distance

        # Write bounds
        self.bounds_x = np.array([min_x, max_x])
        self.bounds_y = np.array([min_y, max_y])
        self.bounds_z = np.array([min_z, max_z])

    # Get and set functions
    def getPosition(self):
        return self.position

    def getScale(self):
        return self.scale

    def getMaterial(self):
        return self.material_index

    def setPosition(self, position):
        self.position = position

    def setScale(self, scale):
        self.scale = scale

    def setMaterial(self, material_index):
        self.material_index = material_index

    # Calculate using the slabs method
    # https://www.cs.cornell.edu/courses/cs4620/2013fa/lectures/03raytracing1.pdf
    def findIntersection(self, P_0, V):
        inverse_direction = np.zeros(3)
        with np.errstate(divide='ignore'):
            inverse_direction = 1 / V
        sign = [int(inverse_direction[0] < 0), int(inverse_direction[1] < 0), int(inverse_direction[2] < 0)]

        # Find tmax and tmin
        tmin = (self.bounds_x[sign[0]] - P_0[0]) * inverse_direction[0]
        tmax = (self.bounds_x[1 - sign[0]] - P_0[0]) * inverse_direction[0]

        # Check y direction
        tymin = (self.bounds_y[sign[1]] - P_0[1]) * inverse_direction[1]
        tymax = (self.bounds_y[1 - sign[1]] - P_0[1]) * inverse_direction[1]

        if tmin > tymax or tymin > tmax:
            return -1

        if tymin > tmin:
            tmin = tymin
        if tymax < tmax:
            tmax = tymax

        # Check z direction
        tzmin = (self.bounds_z[sign[2]] - P_0[2]) * inverse_direction[2]
        tzmax = (self.bounds_z[1 - sign[2]] - P_0[2]) * inverse_direction[2]

        if tmin > tzmax or tzmin > tmax:
            return -1

        if tzmin > tmin:
            tmin = tzmin
        if tzmax < tmax:
            tmax = tzmax

        return tmin

    def getNormal(self, ray):
        epsilon = 1e-6
        p = ray.getP() - self.position
        half_size = np.array([self.bounds_x[1] - self.bounds_x[0], self.bounds_y[1] - self.bounds_y[0],
                              self.bounds_z[1] - self.bounds_z[0]])
        half_size = 0.5 * half_size

        # Calculate the sign of the vector from the center of the cube to the point.
        sign = np.sign(p)

        # Calculate the distance from the point to the edge of the cube.
        distance = np.abs(p) - half_size

        # Calculate the step function.
        step = np.where(distance > epsilon, 1, 0)

        # Return the normal of the surface.
        normal = sign * step
        normal = normalize(normal)
        return normal