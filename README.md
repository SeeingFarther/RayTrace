# Ray Tracing Project

This repository contains code for a Ray Tracing project.

## Installation
You will need to install the following libraries:
- Argparse: pip install argparse
- Pillow:  pip install Pillow
- Numpy: pip install numpy

## Usage

To run the main script with different hyperparameter values, use the `python ray_tracer.py <scene_file_path.txt> <output.png>` command along with the appropriate flags.

### Hyperparameters:


#### Width
To change the width, use the `--width` flag. For example, to generate a image with a width of 1000:

python ray_tracer.py <scene_file_path.txt> <output.png> --width 1000


#### Height
To change the width, use the `--height` flag. For example, to generate a image with a height of 1000:

python ray_tracer.py <scene_file_path.txt> <output.png> --height 1000


#### Transparency
To account for transparency of the objects on the way from the light source to the point, use the `-t` flag. For example:

python ray_tracer.py <scene_file_path.txt> <output.png> -t