import numpy as np
import random
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
    def __init__(self, scene_settings, lights, surfaces, materials, background_color, temp_surfaces):
        self.scene_settings = scene_settings
        self.lights = lights
        self.surfaces = surfaces
        self.materials = materials
        self.background_color = background_color
        self.temp_surfaces = temp_surfaces

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

    def getTempSurfaces(self):
        return self.temp_surfaces

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

    def setTempSurfaces(self, temp_surfaces):
        self.temp_surfaces = temp_surfaces

    def calculateRaysPrecentage(self, ray, light, N, surface):
        # Find plane
        # N · P + d = 0
        N = normalize(N)
        light_position = light.getPosition()
        off = -light_position.dot(N)

        # Find where point with coordinates x = 1, y = 1 on plane using z =  - (Ax + By + D) / C
        z = -(N[0] + N[1] + off) / N[2]
        #z = -(N[0] - distance) / N[2]
        v = np.array([1, 1, z])
        #v = np.array([1, 0, z])
        v = v - light_position

        # Finds perpendicular vector to v
        v = normalize(v)
        u = np.cross(v, N)

        # Normalize vectors
        u = normalize(u)

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

        for i in range(shadow_rays):
            for j in range(shadow_rays):
                # Random points selection to avoid banding
                #random.seed(42)
                x = random.random()
                y = random.random()

                # Calculate distance between points
                point_on_cell = left_up_corner + (cell_height * (i + x)) + (cell_width * (j + y))
                point_on_surface = ray.getIntersectionPoint()
                p = point_on_cell - point_on_surface
                distance = np.linalg.norm(p)
                p_normalized = p / distance

                # Create ray if intersect with surface to know if no light arrives
                t = 0
                transparency = 1
                for surface1 in self.surfaces:
                    # Calculate ray base prevent black spots
                    p = point_on_surface + 0.0002 * p_normalized

                    t = surface1.findIntersection(p, p_normalized)
                    if 0 < t < distance:
                        #transparency *= self.materials[surface.getMaterial() - 1].getTransparency()
                        transparency = 0


                if transparency == 1:
                    # Calculate the ray intensity taking into account the transparency of surfaces the light passes
                    num_of_rays += 1
        sum1 = num_of_rays / np.power(shadow_rays, 2)
        return sum1

    def calculateTransparencyColor(self, ray, max_recursion):
        # Direction of ray
        ray_direction = ray.getDirection()

        # Point where ray starts prevent black spots
        p = ray.getIntersectionPoint() +  0.0002  * ray_direction

        # Find intersection with each surfaces
        color = self.background_color
        t, surface = findIntersection(p, ray_direction, self.surfaces)

        # Have intersection with surface? continue recursively
        if t != np.inf:
            material_index = surface.getMaterial() - 1
            temp_ray = Ray(p, ray_direction, p + t * ray_direction, material_index)
            color = self.calculateColor(temp_ray, self.materials[material_index], surface, max_recursion - 1)

        # Prevent overflow which can happen because of the recursion
        color = np.where(color > 1, 1, color)
        color = np.where(color < 0, 0, color)
        return color

    def calculateReflectanceColor(self, ray, N, max_recursion, material):
        # R is the reflection vector
        # I is the incident vector
        # N is the surface normal vector

        # Direction of reflected ray -> R = I - 2 * N * (N · I)
        ray_direction = ray.getDirection()
        R = N * (-2 * N.dot(ray_direction)) + ray_direction
        R = normalize(R)

        # Point where ray starts prevent black points
        p = ray.getIntersectionPoint()+  0.0002 * R

        # Find intersection with each surfaces
        color = self.background_color * material.getReflectionColor()
        t, surface = findIntersection(p, R, self.surfaces)

        # Have intersection with surface? continue recursively
        if t != np.inf:
            material_index = surface.getMaterial() - 1
            temp_ray = Ray(p, R, p + t * R, material_index)
            color = self.calculateColor(temp_ray, self.materials[material_index], surface, max_recursion - 1)

        # Prevent overflow which can happen because of the recursion
            color = color * material.getReflectionColor()
        color = np.where(color > 1, 1, color)
        color = np.where(color < 0, 0, color)
        return color

    # Calculate specular color
    def calculateSpecularColor(self, light, material, N, L, ray_direction):
        # R - Reflected ray
        # L is the incident vector
        # N is the surface normal vector

        # Calculate reflected ray
        R = N * (N.dot( (L * 2))) - L

        # Calculate specular part
        specular = np.dot(R, -ray_direction)
        specular = np.power(specular, material.getShininess())
        specular = specular * material.getSpecularColor() * light.getSpecularIntensity() * light.getColor()
        return specular

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

        N = N / np.linalg.norm(N)


        # Calculate color as using phong method
        intersection = ray.getIntersectionPoint()
        shadow_color = np.zeros(3)
        for light in self.lights:
            d_color = np.zeros(3)
            L = light.getPosition() - intersection
            L = normalize(L)

            # Calculate diffuse color part
            dot = L.dot(N)
            if dot < 0:
                continue
            d_color = light.getColor() * dot * material.getDiffuseColor()

            R = (N * (2 * N.dot(L))) - L

            # Calculate specular part
            specular = np.dot(R, -ray_direction)
            specular = np.power(specular, material.getShininess())
            specular = specular * material.getSpecularColor() * light.getSpecularIntensity() * light.getColor()
            d_color += specular

            # Calculate diffuse and specular color
            percentage_of_rays = self.calculateRaysPrecentage(ray, light, -L, surface)
            shadow_color += d_color * (
                    (1 - light.getShadowIntensity()) + (percentage_of_rays * light.getShadowIntensity()))

        # Calculate color caused by transparency
        transparency_color = np.zeros(3)
        if material.getTransparency() > 0:
            transparency_color = self.calculateTransparencyColor(ray, max_recursion)

        # Calculate color caused by reflectance
        reflectance_color = np.zeros(3)
        ref = material.getReflectionColor()
        if ref[0] != 0 or ref[1] !=0 or ref[2] != 0:
            reflectance_color = self.calculateReflectanceColor(ray, N, max_recursion, material)

        # Calculate color of surface
        color = (1 - material.getTransparency()) * shadow_color + material.getTransparency() * transparency_color + reflectance_color

        # Prevent overflow which can happen because of the recursion
        color = np.where(color > 1, 1, color)
        color = np.where(color < 0, 0, color)

        return color
