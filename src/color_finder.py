import numpy as np
import random
from light import Light
from material import Material
from scene_settings import SceneSettings
from ray import Ray
from surfaces.cube import Cube
from surfaces.infinite_plane import InfinitePlane
from surfaces.sphere import Sphere
from utilities import *


class ColorFinder:
    def __init__(self, scene_settings, lights, surfaces, materials, background_color, softshadow_func):
        self.scene_settings = scene_settings
        self.lights = lights
        self.surfaces = surfaces
        self.materials = materials
        self.background_color = background_color
        self.softshadow_func = softshadow_func

        # Prevents black spots
        self.black_spots_factor = 0.0008

        # Seed for random (used sha256 for creating seed like in random default)
        seed = 42
        random.seed(seed)

    # Get and set functions
    def getSceneSettings(self):
        return self.scene_settings

    def getLights(self):
        return self.lights

    def getSurfaces(self):
        return self.surfaces

    def getMaterials(self):
        return self.materials

    def getBackgroundColor(self):
        return self.background_color

    def setSceneSettings(self, scene_settings):
        self.scene_settings = scene_settings

    def setLights(self, lights):
        self.lights = lights

    def setSurfaces(self, surfaces):
        self.surfaces = surfaces

    def setMaterials(self, materials):
        self.materials = materials

    def setBackgroundColor(self, background_color):
        self.background_color = background_color

    def calculateRaysPrecentage(self, ray, light, N):
        # Find plane
        # N · P + d = 0 => d = - N · P
        N = normalize(N)
        light_position = light.getPosition()
        distance = -light_position.dot(N)

        # Find where point with coordinates x = 1, y = 1 on plane using z =  - (Ax + By + D) / C
        z = -(N[0] + N[1] + distance) / N[2]
        diagonal_vector = np.array([1, 1, z])
        diagonal_vector = diagonal_vector - light_position

        # Normalize diagonal vector
        diagonal_vector = normalize(diagonal_vector)

        # Finds perpendicular vector to diagonal vector
        up_vector = np.cross(diagonal_vector, N)

        # Normalize up_vector
        up_vector = normalize(up_vector)

        # Finds the left up point of the rectangle
        light_radius = light.getRadius()

        # Move up
        left_up_point = light_position + (up_vector * (-0.5 * light_radius))

        # Move left
        left_up_point += (diagonal_vector * (-0.5 * light_radius))

        # Define a rectangle on that plane, centered at the light source and as wide as the
        # defined light radius. Divide the rectangle into a grid of N*N cells, where N is the number of shadow rays
        shadow_rays = self.scene_settings.getShadowRays()
        cell_proportion = 1.0 / shadow_rays
        rectangle_height = diagonal_vector * light_radius
        rectangle_width = up_vector * light_radius
        cell_height = cell_proportion * rectangle_height
        cell_width = cell_proportion * rectangle_width

        # Aggregate the values of all rays that were cast and count how many of them hit
        # the required point on the surface.
        num_of_rays = 0
        for i in range(shadow_rays):
            for j in range(shadow_rays):
                # Random points selection to avoid banding
                x = random.random()
                y = random.random()

                # Calculate distance between points
                point_on_cell = left_up_point + (cell_height * (i + x)) + (cell_width * (j + y))
                point_on_surface = ray.getIntersectionPoint()
                p = point_on_cell - point_on_surface
                distance = np.linalg.norm(p)

                # Ray direction
                ray_direction = p / distance

                # Calculate ray base (0.0002 prevents black spots)
                p = point_on_surface + self.black_spots_factor * ray_direction

                # Create ray if intersect with surface to know if no light arrives
                transparency_factor = self.softshadow_func(p, ray_direction, distance, self.surfaces, self.materials)

                num_of_rays += (1.0 * transparency_factor)

        percentage = num_of_rays / np.power(shadow_rays, 2)
        return percentage

    def calculateTransparencyColor(self, ray, max_recursion):
        # Direction of ray
        ray_direction = ray.getDirection()

        # Point where ray starts (0.0002 prevents black spots)
        p = ray.getIntersectionPoint() + self.black_spots_factor * ray_direction

        # Find intersection with each surfaces
        color = self.background_color
        t, surface = findIntersection(p, ray_direction, self.surfaces)

        # Have intersection with surface? continue recursively
        if t != np.inf:
            material_index = surface.getMaterial() - 1
            transparency_ray = Ray(p, ray_direction, p + t * ray_direction)
            color = self.calculateColor(transparency_ray, self.materials[material_index], surface, max_recursion - 1)

        # Prevent overflow which can happen because of the recursion
        color = np.clip(color, 0, 1)
        return color

    def calculateReflectanceColor(self, ray, N, max_recursion, material):
        # Direction of reflected ray
        R = calculateReflectionDirection(ray.getDirection(), N)

        # Point where ray starts (0.0002 prevents black spots)
        p = ray.getIntersectionPoint() + self.black_spots_factor * R

        # Find intersection with each surfaces
        color = self.background_color
        t, surface = findIntersection(p, R, self.surfaces)

        # Have intersection with surface? continue recursively
        if t != np.inf:
            material_index = surface.getMaterial() - 1
            reflectance_ray = Ray(p, R, p + t * R)
            color = self.calculateColor(reflectance_ray, self.materials[material_index], surface, max_recursion - 1)

        color = color * material.getReflectionColor()

        # Prevent overflow which can happen because of the recursion
        color = np.clip(color, 0, 1)
        return color

    # Calculate specular color
    def calculateSpecularColor(self, light, material, N, L, ray_direction):
        # Calculate reflected ray
        R = (N * (2 * N.dot(L))) - L

        # Calculate specular part
        specular = R.dot(-ray_direction)
        specular = np.power(specular, material.getShininess())
        specular = specular * material.getSpecularColor() * light.getSpecularIntensity() * light.getColor()
        return specular

    # Calculate color as using phong method
    def calculateSpecularAndDiffuseColor(self, ray, N, material, surface):
        color = np.zeros(3)
        intersection = ray.getIntersectionPoint()
        ray_direction = ray.getDirection()
        for light in self.lights:
            L = light.getPosition() - intersection
            L = normalize(L)

            # Calculate diffuse color part
            dot = L.dot(N)
            if dot < 0:
                continue
            diffuse_and_specular_color = light.getColor() * dot * material.getDiffuseColor()

            # Calculate specular part
            diffuse_and_specular_color += self.calculateSpecularColor(light, material, N, L, ray_direction)

            # Calculate diffuse and specular color
            percentage_of_rays = self.calculateRaysPrecentage(ray, light, -L)
            color += diffuse_and_specular_color * (
                    (1 - light.getShadowIntensity()) + (percentage_of_rays * light.getShadowIntensity()))

        return color

    # Calculate pixel color as instructed in project document
    def calculateColor(self, ray, material, surface, max_recursion):
        # Passed the limit of recursion?
        if max_recursion == 0:
            return self.background_color

        # Init color
        color = np.zeros(3)

        # Get normal
        N = surface.getNormal(ray)

        # Needs the opposite direction of normal?
        ray_direction = ray.getDirection()
        if N.dot(ray_direction) > 0:
            N = -N
        N = normalize(N)

        # Calculate color caused by specular and diffuse
        color += self.calculateSpecularAndDiffuseColor(ray, N, material, surface)

        # Calculate color caused by transparency
        transparency_color = np.zeros(3)
        if material.getTransparency() > 0:
            transparency_color = self.calculateTransparencyColor(ray, max_recursion)

        # Calculate color caused by reflectance
        reflectance_color = np.zeros(3)
        if np.any(material.getReflectionColor() != 0):
            reflectance_color = self.calculateReflectanceColor(ray, N, max_recursion, material)

        # Calculate color of surface
        color = (
                        1 - material.getTransparency()) * color + material.getTransparency() * transparency_color + reflectance_color

        # Prevent overflow which can happen because of the recursion
        color = np.clip(color, 0, 1)
        return color
