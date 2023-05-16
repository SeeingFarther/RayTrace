import numpy as np


def findPixelRays(camera, R_x, R_y):
    V_to = camera.V_to  # look direction vector
    V_up = camera.V_up  # view up vector

    # Calculate view plane center point
    P_0 = camera.position  # camera position
    P_c = P_0 + camera.screen_distance * (V_to / np.linalg.norm(V_to))

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


def calculateColor(ray, lights, materials):
    pass