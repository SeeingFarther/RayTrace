import numpy as np
import random
from Plane import *
from Box import *
from Sphere import *
from Ray import *


# Finds pixel to ray mapping using what we learnt in the lecture
def findPixelRays(camera, R_x, R_y):
    # Look direction vector
    V_to = camera.getLookTo() - camera.getPosition()
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
    P = P_c + (x.reshape(-1, 1) * V_right) - (y.reshape(-1, 1) * plane_V_up)
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
        t = surface[1].findIntersection(base_point, ray_direction)
        # Found closer intersection point?
        if 0 < t < intersect_t:
            intersect_t = t
            intersect_surface = surface

    # Intersection not found?
    if intersect_t == np.inf:
        return None, None

    return intersect_t, intersect_surface


# Calculates the direction of a ray in a fisheye camera in reverse way
def calculateFishEyeRay(camera, P, P_c):
    # Get parameters of sensor plane for theta calculating
    R = np.linalg.norm(P - P_c)
    k = camera.getFisheyeK()
    f = camera.getScreenDistance()

    # Calculate theta
    if k == 0:
        theta = R / f
    elif 0 < k <= 1:
        theta = np.arctan(R * k / f)
        theta = np.degrees(theta / k)
    else:
        theta = np.arcsin(R * k / f)
        theta = np.degrees(theta / k)

    # Point enters through the pin hole?
    if theta > 90:
        return None

    # Calculate ray direction of X_if point
    X_if_direction = P - P_c
    X_if_direction = X_if_direction / np.linalg.norm(X_if_direction)

    # Calculate X_ip
    X_ip = np.tan(np.radians(theta)) * camera.getScreenDistance()

    # Find ray on image plane
    X_ip = P_c + X_if_direction * X_ip
    fish_eye_direction = X_ip - camera.getPosition()
    fish_eye_direction = fish_eye_direction / np.linalg.norm(fish_eye_direction)
    return fish_eye_direction
