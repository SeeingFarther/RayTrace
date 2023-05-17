import numpy as np
from Plane import *


def findPixelRays(camera, R_x, R_y):
    V_to = camera.getLookTo() - camera.getPosition()  # look direction vector
    V_to = V_to / np.linalg.norm(V_to)
    V_up = camera.getUp()  # view up vector

    # Calculate view plane center point
    P_0 = camera.getPosition()  # camera position
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

    return P_normalized


def castRayToCell(set, topLeft, delta_v, delta_u, i, j, intersectionPoint):
    pass


def calculateSoftShadows(set, ray, light, surface, normal):
    light_position = light.getPosition()
    width_radius = light.getWidthRadius()
    shadow_rays = set.getShadowRays()

    # Find plane
    distance = np.dot(normal, light_position)
    light_plane = Plane(normal, distance)

    # Find light position vector on the plane and perpendicular vector to it
    v = light_plane.findProjection(light_position)
    v = v / np.linalg.norm(v)
    u = np.cross(normal, v)
    u = u / np.linalg.norm(u)
    top_left = light_position + (v * (-0.5 * width_radius)) + (u * (-0.5 * width_radius))

    # Define a rectangle on that plane, centered at the light source and as wide as the
    # defined light radius. Divide the rectangle into a grid of N*N cells, where N is the number of shadow rays
    delta = 1.0 / shadow_rays
    rectangle_v = v * width_radius
    rectangle_u = u * width_radius
    delta_v = delta * rectangle_v
    delta_u = delta * rectangle_u * delta

    # Aggregate the values of all rays that were cast and count how many of them hit
    # the required point on the surface.
    light_intensity = 0
    for i in range(shadow_rays):
        for j in range(shadow_rays):
            light_intensity += castRayToCell(set, top_left, delta_v, delta_u, i, j, ray)

    return light_intensity / np.pow(shadow_rays, 2)


def calculateColor(ray, lights, material, surface, background_color):
    color = np.zeros((3, 1), dtype=np.float64)

    # Get normal
    N = surface.getNormal()
    N = N / np.linalg.norm(N)

    # Needs the opposite direction of normal?
    if np.dot(ray.getDirection(), N) > 0:
        N = -N

    # Calculate color as using phong method
    for light in lights:
        L = light.getColor - ray.getIntersectionPoint()
        L = L / np.linalg.norm(L)

        # Calculate diffuse color part
        dot = np.prod(N, L)
        if dot < 0:
            continue
        color = light.getColor() * dot * material.getDiffuseColor()

        # Calculate specular part
        # R - Reflected ray
        R = N * (np.dot((L * 2), N)) - L
        diffuse = np.dot(R, ray.getDirection())
        diffuse = np.pow(diffuse, material.getPhongSpecularity())
        diffuse = diffuse * material.getSpecularColor() * light.getSpecularIntensity()
        color += diffuse

    pass
