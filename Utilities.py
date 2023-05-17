import numpy as np


def findPixelRays(camera, R_x, R_y):
    V_to = camera.V_to - camera.position  # look direction vector
    V_to = V_to / np.linalg.norm(V_to)
    V_up = camera.V_up  # view up vector

    # Calculate view plane center point
    P_0 = camera.position  # camera position
    P_c = P_0 + camera.screen_distance * V_to

    # Calculate view plane right vector
    V_right = np.cross(V_to, V_up)
    V_right = V_right / np.linalg.norm(V_right)

    # Calculate orthonormal view plane up vector
    plane_V_up = np.cross(V_right, V_to)
    plane_V_up = plane_V_up / np.linalg.norm(plane_V_up)

    # Calculate pixel width ratio
    r_x = camera.screen_width / R_x
    screen_height = (R_y / R_x) * camera.screen_width
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


# def calculateSoftShadows(ray, light, surface, normal):
#     # Find plane
#     distance = np.dot(normal, light.position)
#     light_plane = Plane(normal, distance)
#
#     # Find light position on the plane
#     v = light_plane.findProjection(light.position)
#     v = v / np.linalg.norm(v)
#     u = np.cross(normal, v)
#     u = u / np.linalg.norm(u)
#     top_ךeft = light.position + (v * (-0.5 * light.width_radius)) + (u * (-0.5 * light.width_radius))
#
#
# def calculateColor(ray, lights, material, surface, background_color):
#     color = np.zeros((3, 1), dtype=np.float64)
#
#     # Get normal
#     N = surface.getNormal()
#     N = N / np.linalg.norm(N)
#
#     # Needs the opposite direction of normal?
#     if np.dot(ray.direction, N) > 0:
#         N = -N
#
#     # Calculate color as using phong method
#     for light in lights:
#         L = light.position - ray.intersection_point
#         L = L / np.linalg.norm(L)
#
#         # Calculate diffuse color part
#         dot = np.prod(N, L)
#         if dot < 0:
#             continue
#         color = light.lightColor * dot * material.diffuse_color
#
#         # Calculate specular part
#         # R - Reflected ray
#         R = N * (np.dot((L * 2), N)) - L
#         diffuse = np.dot(R, ray.direction)
#         diffuse = np.pow(diffuse, material.phong_specularity)
#         diffuse = diffuse * material.specular_color * light.specular_intensity
#         color += diffuse
#
#     pass
