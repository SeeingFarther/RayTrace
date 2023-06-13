import numpy as np
from ray import *


# Finds pixel to ray mapping using what we learnt in the lecture
def findPixelRays(camera, R_x, R_y):
    # Look direction vector
    V_to = camera.getLookAt() - camera.getPosition()
    V_to = V_to / np.linalg.norm(V_to)

    # View up vector
    V_up = camera.getUp()
    V_up = V_up / np.linalg.norm(V_up)

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
    return P, P_sub


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
        return np.inf, None

    return intersect_t, intersect_surface


# Find transparency factor
def findTransparencyFactor(base_point, ray_direction, distance, surfaces, materials):
    transparency_factor = 1.0

    # Look for intersection with surface
    for surface in surfaces:
        t = surface.findIntersection(base_point, ray_direction)

        # Found intersection point? Mul with the transparency factor
        if 0 < t < distance:
            material = materials[surface.getMaterial() - 1]
            transparency_factor *= material.getTransparency()

    return transparency_factor


# Has intersection
def hasIntersection(base_point, ray_direction, distance, surfaces, materials):
    no_intersection_flag = 1.0

    # Look for intersection with surface
    for surface in surfaces:
        t = surface.findIntersection(base_point, ray_direction)

        # Found intersection point? Mul with the transparency factor
        if 0 < t < distance:
            no_intersection_flag = 0.0
            break

    return no_intersection_flag


def calculateReflectionDirection(I, N):
    # Calculate the reflection direction using the light direction and surface normal
    # R is the reflection vector
    # I is the incident vector
    # N is the surface normal vector
    R = I - (2 * N.dot(I)) * N
    R = normalize(R)
    return R


# Safe normalize
def normalize(V):
    if np.all(V == 0):
        return 0

    return V / np.linalg.norm(V)
