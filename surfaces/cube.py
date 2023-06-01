from .infinite_plane import InfinitePlane
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
        self.max_vec = np.array([max_x, max_y, max_z])
        self.min_vec = np.array([min_x, min_y, min_z])
        self.bounds_x = np.array([min_x, max_x])
        self.bounds_y = np.array([min_y, max_y])
        self.bounds_z = np.array([min_z, max_z])



        # Initialize planes for slabs method
        # self.planes = [
        #     InfinitePlane(np.array([1, 0, 0]), -max_x, material_index)
        #     , InfinitePlane(np.array([1, 0, 0]),-min_x, material_index)
        #     , InfinitePlane(np.array([0, 1, 0]), -max_y, material_index)
        #     , InfinitePlane(np.array([0, 1, 0]), -min_y, material_index)
        #     , InfinitePlane(np.array([0, 0, 1]), -max_z, material_index)
        #     , InfinitePlane(np.array([0, 0, 1]), -min_z, material_index)]

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

    # Calculate using the slab method
    # https://www.cs.cornell.edu/courses/cs4620/2013fa/lectures/03raytracing1.pdf
    def findIntersection(self, P_0, V):
        # t_entry = -np.inf
        # t_exit = np.inf
        #
        # for i in range(0, len(self.planes), 2):
        #     # Reverse planes? (depends on direction of ray)
        #     index = int(np.floor(np.sqrt(i)))
        #     entry_plane = self.planes[i + 1] if V[index] >= 0 else self.planes[i]
        #     exit_plane = self.planes[i] if V[index] >= 0 else self.planes[i + 1]
        #
        #     # Find the intersection points
        #     t_entry_plane = entry_plane.findIntersection(P_0, V)
        #     t_exit_plane = exit_plane.findIntersection(P_0, V)
        #
        #     # Did we find min intersection points?
        #     if t_entry_plane > t_entry:
        #         t_entry = t_entry_plane
        #     if t_exit_plane < t_exit:
        #         t_exit = t_exit_plane
        #
        # # Valid intersections point?
        # if t_entry == -np.inf or t_exit == np.inf:
        #     return -1
        #
        # if t_entry > t_exit:
        #     return -1
        #
        # return t_entry

        inverse_direction = 1 / V
        sign = [int(inverse_direction[0] < 0), int(inverse_direction[1] < 0), int(inverse_direction[2] < 0)]

        tmin = (self.bounds_x[sign[0]] - P_0[0]) * inverse_direction[0]
        tmax = (self.bounds_x[1 - sign[0]] - P_0[0]) * inverse_direction[0]
        tymin = (self.bounds_y[sign[1]] - P_0[1]) * inverse_direction[1]
        tymax = (self.bounds_y[1 - sign[1]] - P_0[1]) * inverse_direction[1]

        if tmin > tymax or tymin > tmax:
            return -1

        if tymin > tmin:
            tmin = tymin
        if tymax < tmax:
            tmax = tymax

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
        # t_entry = np.inf
        # normal = np.array([0, 0, 0])
        # p = ray.getP()
        # ray_direction = ray.getDirection()
        # for plane in self.planes:
        #     t = plane.findIntersection(p, ray_direction)
        #     if t_entry > t > 0:
        #         t_entry = t
        #         normal = plane.getNormal()
        # return normal
        epsilon = 1e-6
        p = ray.getP() - self.position
        half_size = np.array([self.bounds_x[1] - self.bounds_x[0], self.bounds_y[1] - self.bounds_y[0], self.bounds_z[1] - self.bounds_z[0]])
        half_size = 0.5 * half_size

        # Calculate the sign of the vector from the center of the cube to the point.
        sign = np.sign(p)

        # Calculate the distance from the point to the edge of the cube.
        distance = np.abs(p) - half_size

        # Calculate the step function.
        step = np.where(distance > epsilon, 1, 0)

        # Return the normal of the surface.
        normal = sign * step
        return normal / np.linalg.norm(normal)

