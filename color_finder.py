import numpy as np
from camera import Camera
from light import Light
from material import Material
from scene_settings import SceneSettings
from ray import Ray
from surfaces.cube import Cube
from surfaces.infinite_plane import InfinitePlane
from surfaces.sphere import Sphere
from utilities import *


class ColorFinder:
    def __init__(self, scene_settings, lights, surfaces, materials, background_color):
        self.scene_settings = scene_settings
        self.lights = lights
        self.surfaces = surfaces
        self.materials = materials
        self.background_color = background_color

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
        # N · P + d = 0 => # N · P  = -d
        light_position = light.getPosition()
        distance = np.dot(light_position, N)

        # Find where point with coordinates x = 1, y = 0 on plane using z =  - (Ax + By + D) / C
        z = -(N[0] + N[1] - distance) / N[2]
        v = np.array([1, 1, z])
        v = v - light_position

        # Finds perpendicular vector to v
        u = np.cross(N, v)

        # Normalize vectors
        u = u / np.linalg.norm(u)
        v = v / np.linalg.norm(v)

        # Finds the left up corner of the rectangle
        light_radius = light.getRadius()
        left_up_corner = light_position + (u * (-0.5 * light_radius)) + (v * (-0.5 * light_radius))

        # Define a rectangle on that plane, centered at the light source and as wide as the
        # defined light radius. Divide the rectangle into a grid of N*N cells, where N is the number of shadow rays
        shadow_rays = self.scene_settings.getShadowRays()
        cell_proportion = 1.0 / shadow_rays
        rectangle_height = v * light_radius
        rectangle_width = u * light_radius
        cell_height = cell_proportion * rectangle_height
        cell_width = cell_proportion * rectangle_width

        # Aggregate the values of all rays that were cast and count how many of them hit
        # the required point on the surface.
        num_of_rays = 0
        np.random.seed(42)
        random_values = np.random.rand(shadow_rays, shadow_rays, 2)
        for i in range(shadow_rays):
            for j in range(shadow_rays):
                # Random points selection to avoid banding
                x = random_values[i, j, 0]
                y = random_values[i, j, 1]

                # Calculate distance between points
                point_on_cell = left_up_corner + cell_height * (i + x) + cell_width * (j + y)
                point_on_surface = ray.getIntersectionPoint()
                p = point_on_cell - point_on_surface
                distance = np.linalg.norm(p)

                # Finds direction of ray
                ray_direction = p / distance

                # Calculate ray base (prevents black spots)
                p = point_on_surface + ray_direction * 0.001

                # Create ray if intersect with surface to know if no light arrives
                transparency_factor = findTransperancyFactor(p, ray_direction, distance, self.surfaces, self.materials)

                # Calculate the ray intensity taking into account the transparency of surfaces the light passes
                num_of_rays += transparency_factor

        return num_of_rays / np.power(shadow_rays, 2)

    def calculateTransparencyColor(self, ray, max_recursion):
        # Direction of ray
        ray_direction = ray.getDirection()

        # Point where ray starts (prevent black spots)
        p = ray.getIntersectionPoint() + 0.001 * ray_direction

        # Find intersection with each surfaces
        color = self.background_color
        t, surface = findIntersection(p, ray_direction, self.surfaces)

        # Have intersection with surface? continue recursively
        if t is not None:
            material_index = surface.getMaterial() - 1
            transparency_ray = Ray(p, ray_direction, p + t * ray_direction, material_index)
            color = self.calculateColor(transparency_ray, self.materials[material_index], surface, max_recursion - 1)

        # Prevent overflow which can happen because of the recursion
        color = np.where(color > 1, 1, color)
        return color

    def calculateReflectanceColor(self, ray, N, max_recursion):
        # Calculate reflected ray direction
        ray_direction = calculateReflectionDirection(ray.getDirection(), N)

        # Point where ray starts prevent black points
        p = ray.getIntersectionPoint() + 0.001 * ray_direction

        # Find intersection with each surfaces
        color = self.background_color
        t, surface = findIntersection(p, ray_direction, self.surfaces)

        # Have intersection with surface? continue recursively
        if t is not None:
            material_index = surface.getMaterial() - 1
            reflected_ray = Ray(p, ray_direction, p + t * ray_direction, material_index)
            color = self.calculateColor(reflected_ray, self.materials[material_index], surface, max_recursion - 1)

        # Prevent overflow which can happen because of the recursion
        color = color * self.materials[ray.getIntersectionSurfaceMaterialIndex()].getReflectionColor()
        color = np.where(color > 1, 1, color)
        return color

    # Calculate specular color
    def calculateSpecularColor(self, light, material, N, L, ray_direction):
        # Calculate reflected ray direction
        reflected_ray = N * (np.dot(N, (L * 2))) - L

        # Calculate specular part
        specular = np.dot(reflected_ray, -ray_direction)
        specular = np.power(specular, material.getShininess())
        specular = specular * material.getSpecularColor() * light.getSpecularIntensity() * light.getColor()
        return specular

    # Calculate diffuse color
    def calculateDiffuseColor(self, light, material, tetha):
        return light.getColor() * tetha * material.getDiffuseColor()

    # Calculate surface color using phong method
    def calculateDiffuseAndSpecular(self, ray, material, N):
        color = np.zeros(3, dtype=np.float64)
        ray_direction = ray.getDirection()
        intersection = ray.getIntersectionPoint()
        for light in self.lights:
            # Finds light ray
            L = light.getPosition() - intersection
            L = L / np.linalg.norm(L)
            dot = np.dot(L, N)
            if dot < 0:
                continue

            diffuse_specular_color = self.calculateDiffuseColor(light, material, dot)

            # Calculate specular color
            diffuse_specular_color += self.calculateSpecularColor(light, material, N, L, ray_direction)

            # Calculate diffuse and specular color
            percentage_of_rays = self.calculateRaysPrecentage(ray, light, -L)
            color += diffuse_specular_color * (
                    (1 - light.getShadowIntensity()) + percentage_of_rays * light.getShadowIntensity())
        return color

    def calculateColor(self, ray, material, surface, max_recursion):
        # Passed the limit of recursion?
        if max_recursion == 0:
            return self.background_color

        # Calculate color caused by transparency
        transparency_color = np.zeros(3, dtype=np.float64)
        if material.getTransparency() > 0:
            transparency_color = self.calculateTransparencyColor(ray, max_recursion)

        # Init color
        color = np.zeros(3, dtype=np.float64)

        # Get normal
        N = surface.getNormal(ray)

        # Needs the opposite direction of normal?
        ray_direction = ray.getDirection()
        if np.dot(N, ray_direction) > 0:
            N = -N

        # Normalize normal
        N /= np.linalg.norm(N)

        # Calculate color caused by reflectance
        reflectance_color = np.zeros(3, dtype=np.float64)
        if np.any(material.getReflectionColor() > 0):
            reflectance_color = self.calculateReflectanceColor(ray, N, max_recursion)

        color = self.calculateDiffuseAndSpecular(ray, material, N)

        # Calculate color of surface
        color = (1 - material.getTransparency()) * color \
                + material.getTransparency() * transparency_color + reflectance_color

        # Prevent overflow which can happen because of the recursion
        color = np.where(color > 1, 1, color)
        return color
