import numpy as np
import random
from surfaces.cube import Cube
from surfaces.infinite_plane import InfinitePlane
from surfaces.sphere import Sphere
from ray import *


# Finds pixel to ray mapping using what we learnt in the lecture
def findPixelRays(camera, R_x, R_y):
    # Look direction vector
    V_to = camera.getLookAt() - camera.getPosition()
    V_to = V_to / np.linalg.norm(V_to)

    # View up vector
    V_up = camera.getUp()

    # Calculate view plane center point
    P_0 = camera.getPosition()
    P_c = P_0 + camera.getScreenDistance() * V_to

    # Calculate view plane right vector
    V_right = np.cross(V_to, V_up)
    V_right = V_right / np.linalg.norm(V_right)

    # Calculate orthonormal view plane up vector
    plane_V_up = np.cross(V_right, V_to)
    plane_V_up = plane_V_up / np.linalg.norm(plane_V_up)

    # Calculate pixel width ratio
    screen_width = camera.getScreenWidth()
    r_x = screen_width / R_x
    screen_height = (R_y / R_x) * screen_width
    r_y = screen_height / R_y

    # Find each screen pixel coordinates
    i_matrix = np.tile(np.arange(R_x), (R_y, 1)).T
    j_matrix = np.tile(np.arange(R_y), (R_x, 1))
    x = r_x * (j_matrix - np.floor(R_x / 2))
    y = r_y * (i_matrix - np.floor(R_y / 2))
    P = P_c - (x.reshape(-1, 1) * V_right) - (y.reshape(-1, 1) * plane_V_up)
    P = P.reshape(R_x, R_y, 3)

    # Calculate the subtraction of each vector in the matrix with P_0
    P_sub = P - P_0

    # Calculate the norm of each vector
    P_norm = np.linalg.norm(P_sub, axis=2)

    # Calculate the normalized vector of the subtraction of each vector to P_0
    P_normalized = P_sub / P_norm[:, :, np.newaxis]

    return P, P_normalized


# Tries to find minimum intersection point with one of the surfaces
def findIntersection(base_point, ray_direction, surfaces):
    intersect_t = np.inf
    intersect_surface = None

    # Look for intersection with surface
    for surface in surfaces:
        t = surface.findIntersection(base_point, ray_direction)
        # Found closer intersection point?
        if 0 < t < intersect_t:
            intersect_t = t
            intersect_surface = surface

    # Intersection not found?
    if intersect_t == np.inf:
        return None, None

    return intersect_t, intersect_surface


# find transperancy factor
def findTransperancyFactor(base_point, ray_direction, distance, surfaces, materials):
    intersect_t = np.inf

    # Look for intersection with surface
    for surface in surfaces:
        t = surface.findIntersection(base_point, ray_direction)
        # Found closer intersection point?
        if 0 < t < intersect_t:
            intersect_t = 0

    # Intersection not found?
    if intersect_t == np.inf:
        return 0

    return 1


def calculateReflectionDirection( I, N):
    # Calculate the reflection direction using the light direction and surface normal
    R = I - (2 * np.dot(I, N)) * N
    R /= np.linalg.norm(R)
    return R