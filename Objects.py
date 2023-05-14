import numpy as np


class Camera:
    def __init__(self, position, V_to, V_up, screen_distance, screen_width, use_fisheye, fisheye_k):
        self.position = position
        self.V_to = V_to
        self.V_up = V_up
        self.screen_distance = screen_distance
        self.screen_width = screen_width
        self.use_fisheye = use_fisheye
        self.fisheye_k = fisheye_k


class Set:
    def __init__(self, background_color, shadow_rays, max_recursions):
        self.background_color = background_color
        self.shadow_rays = shadow_rays
        self.max_recursions = max_recursions


class Material:
    def __init__(self, diffuse_color, specular_color, reflection_color, phong_specularity, transparency):
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.reflection_color = reflection_color
        self.phong_specularity = phong_specularity
        self.transparency = transparency


class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    # Calculate intersection between the ray and the sphere using geometric method
    def intersect(self, P_0, V):
        # Calculate L and T_ca
        L = self.center - P_0
        T_ca = L.dot(V)
        if T_ca < 0:
            return 0

        # Calculate d^2
        d_squared = L.dot(L) - (T_ca * T_ca)
        if d_squared > self.radius * self.radius:
            return 0

        # Calculate T_hc
        T_hc = np.sqrt(self.radius * self.radius - d_squared)
        t1 = T_ca - T_hc
        t2 = T_ca + T_hc

        # Checks for the closet positive from the two intersection points else return zero
        if t1 <= 0 and t2 <= 0:
            return 0

        if t1 > t2:
            t1, t2 = t2, t1

        if t1 < 0:
            t1 = t2
        return t1


class Plane:
    def __init__(self, normal, offset, material):
        self.normal = normal
        self.offset = offset
        self.material = material

    # Calculate intersection between the ray and the plane using algebraic method
    def intersect(self, P_0, V):
        div = V.dot(self.normal)
        prod = P_0.dot(self.normal) + self.offset
        t = -prod / div
        return t


class Box:
    def __init__(self, position, scale, material):
        self.position = position
        self.scale = scale
        self.material = material


class Light:
    def __init__(self, position, color, specular_intensity, shadow_intensity, width_radius):
        self.position = position
        self.color = color
        self.specular_intensity = specular_intensity
        self.shadow_intensity = shadow_intensity
        self.width_radius = width_radius
