import numpy as np
import random
from Set import *
from Plane import *
from Box import *
from Sphere import *
from Material import *
from Light import *
from Ray import *
from Utilities import *


class ColorFinder:
    def __init__(self, set, lights, surfaces, materials, background_color):
        self.set = set
        self.lights = lights
        self.surfaces = surfaces
        self.materials = materials
        self.background_color = background_color
        self.temp_surfaces = None

    # Get and set functions
    def getSet(self):
        return self.set

    def getLights(self):
        return self.lights

    def getSurfaces(self):
        return self.surfaces

    def getMaterials(self):
        return self.materials

    def getBackgroundColor(self):
        return self.background_color

    def getTempSurfaces(self):
        return self.temp_surfaces

    def setSet(self, set):
        self.set = set

    def setLights(self, lights):
        self.lights

    def setSurfaces(self, surfaces):
        self.surfaces = surfaces

    def setMaterials(self, materials):
        self.materials = materials

    def setBackgroundColor(self, background_color):
        self.background_color = background_color

    def setTempSurfaces(self, temp_surfaces):
        self.temp_surfaces = temp_surfaces

    def calculateRaysPrecentage(self, ray, light, N):
        # Find plane
        # N · P + d = 0
        light_position = light.getPosition()
        distance = np.dot(light_position, N)

        # Find where point with coordinates x = 1, y = 1 on plane using z =  - (Ax + By + D) / C
        z = -(N[0] + N[1] - distance) / N[2]
        v = np.array([1, 1, z])
        v = v - light_position

        # Finds perpendicular vector to v
        u = np.cross(N, v)

        # Normalize vectors
        u = u / np.linalg.norm(u)
        v = v / np.linalg.norm(v)

        # Finds the left up corner of the rectangle
        light_width_radius = light.getWidthRadius()
        left_up_corner = light_position + (u * (-0.5 * light_width_radius)) + (v * (-0.5 * light_width_radius))

        # Define a rectangle on that plane, centered at the light source and as wide as the
        # defined light radius. Divide the rectangle into a grid of N*N cells, where N is the number of shadow rays
        shadow_rays = self.set.getShadowRays()
        cell_proportion = 1 / shadow_rays
        rectangle_height = v * light_width_radius
        rectangle_width = u * light_width_radius
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
                p_normalized = p / distance

                # Create ray if intersect with surface to know if no light arrives
                t = 0
                intersect = False
                for surface in self.surfaces:
                    # Calculate ray base prevent black spots
                    p = point_on_surface + p_normalized * 0.0002

                    t = surface[1].findIntersection(p, p_normalized)
                    if 0 < t < distance:
                        intersect = True
                        break

                if not intersect:
                    num_of_rays += 1

        return num_of_rays / np.power(shadow_rays, 2)

    def calculateTransparencyColor(self, ray, max_recursion):
        # Direction of ray
        ray_direction = ray.getDirection()

        # Point where ray starts prevent black spots
        p = ray.getIntersectionPoint() + 0.0002 * ray_direction

        # Find intersection with each surfaces
        color = self.background_color
        t, surface = findIntersection(p, ray_direction, self.temp_surfaces)

        # Have intersection with surface? continue recursively
        if t is not None:
            #self.temp_surfaces.remove(surface)
            material_index = surface[1].getMaterial() - 1
            temp_ray = Ray(p, ray_direction, p + t * ray_direction, material_index)
            color = self.calculateColor(temp_ray, self.materials[material_index], surface[1], max_recursion - 1)

        # Prevent overflow which can happen because of the recursion
        color = np.where(color > 1, 1, color)
        return color

    def calculateReflectanceColor(self, ray, N, max_recursion):
        # R is the reflection vector
        # I is the incident vector
        # N is the surface normal vector

        # Direction of reflected ray -> R = I - 2 * N * (N · I)
        ray_direction = ray.getDirection()
        ray_direction = N * (-2 * np.dot(N, ray_direction)) + ray_direction
        ray_direction = ray_direction / np.linalg.norm(ray_direction)

        # Point where ray starts prevent black points
        p = ray.getIntersectionPoint() + 0.0002 * ray_direction

        # Find intersection with each surfaces
        color = self.background_color
        t, surface = findIntersection(p, ray_direction, self.surfaces)

        # Have intersection with surface? continue recursively
        if t is not None:
            material_index = surface[1].getMaterial() - 1
            temp_ray = Ray(p, ray_direction, p + t * ray_direction, material_index)
            color = self.calculateColor(temp_ray, self.materials[material_index], surface[1], max_recursion - 1)

        # Prevent overflow which can happen because of the recursion
        color = color * self.materials[ray.getIntersectionSurfaceMaterialIndex()].getReflectionColor()
        color = np.where(color > 1, 1, color)
        return color

    # Calculate specular color
    def calculateSpecularColor(self, light, material, N, L, ray_direction):
        # R - Reflected ray
        # L is the incident vector
        # N is the surface normal vector

        # Calculate reflected ray
        R = N * (np.dot(N, (L * 2))) - L

        # Calculate specular part
        specular = np.dot(R, -ray_direction)
        specular = np.power(specular, material.getPhongSpecularity())
        specular = specular * material.getSpecularColor() * light.getSpecularIntensity() * light.getColor()
        return specular

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

        N = N / np.linalg.norm(N)

        # Calculate color caused by reflectance
        reflectance_color = np.zeros(3, dtype=np.float64)
        if np.any(material.getReflectionColor() > 0):
            reflectance_color = self.calculateReflectanceColor(ray, N, max_recursion)

        # Calculate color as using phong method
        intersection = ray.getIntersectionPoint()
        for light in self.lights:
            L = light.getPosition() - intersection
            L = L / np.linalg.norm(L)

            # Calculate diffuse color part
            dot = np.dot(L, N)
            if dot < 0:
                continue
            diffuse_specular_color = light.getColor() * dot * material.getDiffuseColor()

            # Calculate specular color
            diffuse_specular_color += self.calculateSpecularColor(light, material, N, L, ray_direction)

            # Calculate diffuse and specular color
            percentage_of_rays = self.calculateRaysPrecentage(ray, light, -L)
            color += diffuse_specular_color * (
                    (1 - light.getShadowIntensity()) + percentage_of_rays * light.getShadowIntensity())

        # Calculate color of surface
        color = (1 - material.getTransparency()) * color \
                + material.getTransparency() * transparency_color + reflectance_color

        # Prevent overflow which can happen because of the recursion
        color = np.where(color > 1, 1, color)
        return color
