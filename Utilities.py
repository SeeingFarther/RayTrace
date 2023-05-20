import numpy as np
import random
from Set import *
from Plane import *
from Box import *
from Sphere import *
from Material import *
from Light import *
from Ray import *


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


def find_intersection(base_point, direction, surfaces):
    intersect_t = float("inf")
    intersect_surface = None

    # Look for intersection with surface
    for surface in surfaces:
        t = surface[1].intersect(base_point, direction)
        if t < intersect_t and t > 0:
            intersect_t = t
            intersect_surface = surface

    # Intersection not found?
    if intersect_t == float("inf"):
        return None, None

    return intersect_t, intersect_surface


def calculateRaysPrecentage(surfaces, set, ray, light, N):
    width_radius = light.getWidthRadius()
    shadow_rays = set.getShadowRays()
    light_position = light.getPosition()

    # Find plane
    distance = N.dot(light_position)
    light_plane = Plane(N, distance, 0)

    # Find light position vector on the plane and perpendicular vector to it
    v = light_plane.findProjection(light_position)
    v = v / np.linalg.norm(v)
    u = np.cross(N, v)
    u = u / np.linalg.norm(u)
    left_up_corner = light_position + (v * (-0.5 * width_radius)) + (u * (-0.5 * width_radius))

    # Define a rectangle on that plane, centered at the light source and as wide as the
    # defined light radius. Divide the rectangle into a grid of N*N cells, where N is the number of shadow rays
    cell_proportion = 1.0 / shadow_rays
    rectangle_height = v * width_radius
    rectangle_width = u * width_radius
    cell_height = cell_proportion * rectangle_height
    cell_width = cell_proportion * rectangle_width

    # Aggregate the values of all rays that were cast and count how many of them hit
    # the required point on the surface.
    num_of_rays = 0
    random.seed(42)
    for i in range(shadow_rays):
        for j in range(shadow_rays):
            # Random points selection to avoid banding
            x = random.random()
            y = random.random()

            # Calculate distance between points
            point_on_cell = left_up_corner + cell_height * (i + x) + cell_width * (j + y)
            point_on_surface = ray.getIntersectionPoint()
            p = point_on_cell - point_on_surface
            distance = np.linalg.norm(p)

            # Create ray if intersect with surface(to know be no light arrives)
            t = 0
            intersect = False
            for surface in surfaces:
                t = surface[1].intersect(point_on_surface * 0.001, p)
                if 0 < t < distance:
                    intersect = True
                    break

            if not intersect:
                num_of_rays += 1

    return num_of_rays / np.power(shadow_rays, 2)


def calculateTransparencyColor(ray, set, surfaces, materials, lights, background_color, max_recursion):
    # Direction of ray
    direction = ray.getDirection()

    # Point where ray starts
    base_point = ray.getIntersectionPoint() + 0.001 * direction

    # Find intersection with each surfaces
    color = background_color
    t, surface = find_intersection(base_point, direction, surfaces)

    # Have intersection with surface? continue recursively
    if t is not None:
        material_index = surface[1].getMaterial() - 1
        ray_temp = Ray(base_point, direction, base_point + t * direction, material_index)
        color = calculateColor(ray_temp, set, surfaces, materials, lights, materials[material_index], surface[1], background_color,
                               max_recursion - 1)

    # Prevent overflow which can happen because of the recursion
    color = np.where(color > 1, 1, color)
    return color


def calculateReflectanceColor(ray, N, set, surfaces, materials, lights, background_color, max_recursion):
    # Direction of reflected ray -> R = I - 2 * N * (N dot I)
    # R is the reflection vector
    # I is the incident vector
    # N is the surface normal vector
    direction = N * (-2 * ray.direction_vector.dot(N)) + ray.getDirection()
    direction = direction / np.linalg.norm(direction)

    # Point where ray starts
    base_point = ray.getIntersectionPoint() + 0.001 * direction

    # Find intersection with each surfaces
    color = background_color
    t, surface = find_intersection(base_point, direction ,surfaces)

    # Have intersection with surface? continue recursively
    if t is not None:
        material_index = surface[1].getMaterial() - 1
        ray_temp = Ray(base_point, direction, base_point + t * direction, material_index)
        color = calculateColor(ray_temp, set, surfaces, materials, lights, materials[material_index], surface[1], background_color,
                               max_recursion - 1)

    # Prevent overflow which can happen because of the recursion
    color = np.where(color > 1, 1, color)
    return color


def calculateColor(ray, set, surfaces, materials, lights, material, surface, background_color, max_recursion):
    # Passed the limit of recursion?
    if max_recursion == 0:
        return background_color

    color = np.zeros((3, 1), dtype=np.float64)

    # Get normal
    N = surface.getNormal()
    N = N / np.linalg.norm(N)

    # Needs the opposite direction of normal?
    if ray.getDirection().dot(N) > 0:
        N = -N

    # Calculate color as using phong method
    for light in lights:
        L = light.getPosition() - ray.getIntersectionPoint()
        L = L / np.linalg.norm(L)

        # Calculate diffuse color part
        dot = N.dot(L)
        if dot < 0:
            continue
        color = light.getColor() * dot * material.getDiffuseColor()

        # Calculate specular part
        # R - Reflected ray
        # L is the incident vector
        # N is the surface normal vector
        R = N * ((L * 2).dot(N)) - L
        specular = R.dot(-ray.getDirection())
        specular = np.power(specular, material.getPhongSpecularity())
        specular = specular * material.getSpecularColor() * light.getSpecularIntensity()
        color += specular

        # Calculate diffuse and specular color
        percentage_of_rays = calculateRaysPrecentage(surfaces, set, ray, light, -L)
        light_intensity = (1 - light.getShadowIntensity()) + percentage_of_rays * light.getShadowIntensity()
        color = color * light_intensity

    # Calculate color caused by transparency
    transparency_color = background_color
    if material.getTransparency() > 0:
        transparency_color = calculateTransparencyColor(ray, set, surfaces, materials, lights, background_color,
                                                        max_recursion)
    # Calculate color caused by reflectance
    reflectance_color = background_color
    if np.any(material.getReflectionColor() > 0):
        reflectance_color = calculateReflectanceColor(ray, N, set, surfaces, materials, lights, background_color,
                                                      max_recursion)

    # Calculate color of surface
    color = (1 - material.getTransparency()) * color + material.getTransparency() * transparency_color + reflectance_color

    # Prevent overflow which can happen because of the recursion
    color = np.where(color > 1, 1, color)
    return color
