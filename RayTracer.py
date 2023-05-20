import numpy as np
import sys
import math
from PIL import Image
import time
import re
from Camera import *
from Set import *
from Plane import *
from Box import *
from Sphere import *
from Material import *
from Light import *
from Utilities import *
from Ray import *


class RayTracer:

    def __init__(self, width=500, height=500):
        self.image_width = width
        self.image_height = height
        self.camera = None
        self.set = None
        self.rays_directions = []
        self.surfaces = []
        self.materials = []
        self.lights = []
        self.objects = []

    # Get and set functions
    def getWidth(self):
        return self.image_width

    def getHeight(self):
        return self.image_height

    def getCamera(self):
        return self.camera

    def getSet(self):
        return self.set

    def getRaysDirections(self):
        return self.rays_directions

    def getSurfaces(self):
        return self.surfaces

    def getMaterials(self):
        return self.materials

    def getLights(self):
        return self.lights

    def getObjects(self):
        return self.objects

    def setWidth(self, width):
        self.image_width = width

    def setHeight(self, height):
        self.image_height = height

    def setCamera(self, camera):
        self.camera = camera

    def setSet(self, set):
        self.set = set

    def setRaysDirections(self, rays_directions):
        self.rays_directions = rays_directions

    def setSurfaces(self, surfaces):
        self.surfaces = surfaces

    def setMaterials(self, materials):
        self.materials = materials

    def setLights(self, lights):
        self.lights = lights

    def setObjects(self, objects):
        self.objects = objects

    def parseScene(self, scene_file_path):
        with open(scene_file_path) as f:
            lines = f.readlines()

        for lineNum, line in enumerate(lines):
            line = line.strip()
            if line == '' or line[0] == '#':
                continue

            code = line[:3].lower()
            params = line[3:].strip().lower()
            params = re.sub('\s+', ' ', params).split()

            if code == 'cam':
                # Parse camera parameters
                object_params = {
                    'position': np.array([float(params[0]), float(params[1]), float(params[2])], dtype=np.float64),
                    'look_at': np.array([float(params[3]), float(params[4]), float(params[5])], dtype=np.float64),
                    'up_vector': np.array([float(params[6]), float(params[7]), float(params[8])], dtype=np.float64),
                    'screen_distance': float(params[9]),
                    'screen_width': float(params[10]),
                    'use_fisheye': params[11] == 'true',
                    'fisheye_k': float(params[12]) if len(params) > 12 else 0.5
                }

                # Create camera
                object = Camera(object_params['position'], object_params['look_at'],
                                object_params['up_vector'], object_params['screen_distance'],
                                object_params['screen_width'], object_params['use_fisheye'], object_params['fisheye_k'])
                self.camera = object
                print(f'Parsed camera parameters (line {lineNum})')

            elif code == 'set':
                # Parse general settings parameters
                object_params = {
                    'background_color': np.array([float(params[0]), float(params[1]), float(params[2])],
                                                 dtype=np.float64),
                    'shadow_rays': int(params[3]),
                    'max_recursions': int(params[4])
                }

                # Create set
                object = Set(object_params['background_color'], object_params['shadow_rays'],
                             object_params['max_recursions'])
                self.set = object
                print(f'Parsed general settings (line {lineNum})')

            elif code == "mtl":
                # Parse material
                object_params = {
                    'diffuse_color': np.array([float(params[0]), float(params[1]), float(params[2])], dtype=np.float64),
                    'specular_color': np.array([float(params[3]), float(params[4]), float(params[5])],
                                               dtype=np.float64),
                    'reflection_color': np.array([float(params[6]), float(params[7]), float(params[8])],
                                                 dtype=np.float64),
                    'phong_specularity': float(params[9]),
                    'transparency': float(params[10])
                }

                # Create material
                object = Material(object_params['diffuse_color'], object_params['specular_color'],
                                  object_params['reflection_color'],
                                  object_params['phong_specularity'], object_params['transparency'])
                self.materials.append(object)
                print(f'Parsed material (line {lineNum})')

            elif code == 'sph':
                # Parse sphere parameters
                object_params = {
                    'position': np.array([float(params[0]), float(params[1]), float(params[2])], dtype=np.float64),
                    'radius': float(params[3]),
                    'material_index': int(params[4])
                }

                # Create sphere
                object = Sphere(object_params['position'], object_params['radius'], object_params['material_index'])
                self.surfaces.append((code, object))
                print(f'Parsed sphere (line {lineNum})')

            elif code == 'pln':
                # Parse plane parameters
                object_params = {
                    'normal': np.array([float(params[0]), float(params[1]), float(params[2])], dtype=np.float64),
                    'offset': float(params[3]),
                    'material_index': int(params[4])
                }

                # Create plane
                object = Plane(object_params['normal'], object_params['offset'], object_params['material_index'])
                self.surfaces.append((code, object))
                print(f'Parsed plane (line {lineNum})')

            elif code == 'box':
                # Parse box parameters
                object_params = {
                    'position': np.array([float(params[0]), float(params[1]), float(params[2])], dtype=np.float64),
                    'scale': float(params[3]),
                    'material_index': int(params[4])
                }

                # Create box
                object = Box(object_params['position'], object_params['scale'], object_params['material_index'])
                self.surfaces.append((code, object))
                print(f'Parsed box (line {lineNum})')

            elif code == 'lgt':
                # Parse light parameters
                object_params = {
                    'position': np.array([float(params[0]), float(params[1]), float(params[2])], dtype=np.float64),
                    'color': np.array([float(params[3]), float(params[4]), float(params[5])], dtype=np.float64),
                    'specular_intensity': float(params[6]),
                    'shadow_intensity': float(params[7]),
                    'width_radius': float(params[8])
                }

                # Create light
                object = Light(object_params['position'], object_params['color'],
                               object_params['specular_intensity'], object_params['shadow_intensity'],
                               object_params['width_radius'])
                self.lights.append(object)
                print(f'Parsed light (line {lineNum})')

            else:
                print(f'ERROR: Did not recognize object: {code} (line {lineNum})')
                continue

            self.objects.append((code, object))
        # It is recommended that you check here that the scene is valid,
        # for example camera settings and all necessary materials were defined.
        print(f'Finished parsing scene file {scene_file_path}')

    def renderScene(self, outputFileName):
        start_time = int(round(time.time() * 1000))

        # Create a numpy array to hold the pixel data:
        rgb_data = np.zeros((self.image_height, self.image_width, 3), dtype=np.uint8)

        # Find for each pixel is color
        P_0 = self.camera.getPosition()
        for row in range(self.image_height):
            for col in range(self.image_width):
                color = self.set.getBackgroundColor()

                # Find intersection with each surfaces
                t, surface = find_intersection(P_0, self.rays_directions[row, col], self.surfaces)

                if t is not None:
                    material_index = surface[1].getMaterial() - 1
                    ray = Ray(self.camera.getPosition(), self.rays_directions[row, col], self.camera.getPosition() + t * self.rays_directions[row, col], material_index)
                    color = calculateColor(ray, self.set, self.surfaces, self.materials, self.lights, self.materials[material_index], surface[1], self.set.getBackgroundColor(), self.set.getMaxRecursions())
                rgb_data[row, col, :] = (color[:] * 255)

        # Save the image to file
        img = Image.fromarray(rgb_data, 'RGB')
        img.save(outputFileName)

        end_time = int(round(time.time() * 1000))
        render_time = (end_time - start_time) / 1000
        print(f'Finished rendering scene in {render_time} seconds.')


if __name__ == "__main__":
    tracer = RayTracer()
    # if len(sys.argv) < 3:
    #     print('Not enough arguments provided. Please specify an input scene file and an output image file for rendering.')
    #     exit(1)
    # scene_file_path = sys.argv[1]
    # output_file_path = sys.argv[2]
    #
    # if len(sys.argv) > 3:
    #     tracer.setWidth(int(sys.argv[3]))
    #
    # if len(sys.argv) > 4:
    #     tracer.setHeight(int(sys.argv[4]))
    scene_file_path = './Pool.txt'
    tracer.parseScene(scene_file_path)
    tracer.setRaysDirections(findPixelRays(tracer.camera, tracer.image_width, tracer.image_height))
    tracer.renderScene('test.png')
    print("helllssssssssssssssss")