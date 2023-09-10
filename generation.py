import cv2
import numpy as np
from sklearn.cluster import KMeans
from octree_color_quantizer.octree_quantizer import OctreeQuantizer
from octree_color_quantizer.color import Color

MAX_HEIGHT = 720
MAX_WIDTH = 1280

def clamp_size(image):
    """
    Given an image, resizes it to a maximum of MAX_HEIGHT x MAX_WIDTH.
    """
    height, width, _ = image.shape
    if height * width > MAX_HEIGHT * MAX_WIDTH:
        scale = min(MAX_HEIGHT / height, MAX_WIDTH / width)
        image = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)


def image_to_pixels(image_path):
    """
    Given an image path, returns a h*w x 3 matrix of rgb values for pixels in the image.
    """
    image = cv2.imread(image_path)
    clamp_size(image)
    im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape
    pixels = im_rgb.reshape(height*width, 3)
    return pixels


# num_colors: string input
# given an image path and number of colors, returns a list of hex color codes
def kmeans_generation(image_path, num_colors):
    pixels = image_to_pixels(image_path)
    kmeans = KMeans(n_clusters=int(num_colors), init='k-means++', random_state=0, n_init='auto')
    kmeans.fit(pixels)
    rgb_colors = kmeans.cluster_centers_.astype(int)
    palette = list('#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in rgb_colors)
    return palette


def median_cut(image_path, num_colors):
    pixels = image_to_pixels(image_path)
    
    def split_cube(cube):
        # find the color channel in the image with the greatest range
        r_range = np.max(cube[:, 0]) - np.min(cube[:, 0])
        g_range = np.max(cube[:, 1]) - np.min(cube[:, 1])
        b_range = np.max(cube[:, 2]) - np.min(cube[:, 2])

        if r_range >= g_range and r_range >= b_range:
            highest_range_channel = 0
        elif g_range >= r_range and g_range >= b_range:
            highest_range_channel = 1
        else: # blue
            highest_range_channel = 2

        # sort the pixels by the highest range channel
        cube = cube[cube[:, highest_range_channel].argsort()]
        # find the median and cut by that pixel
        median = cube.shape[0] // 2
        left = cube[0:median]
        right = cube[median:]
        return left, right

    # split the largest cube until the number of colors is reached
    cubes = [np.array(pixels)]
    while len(cubes) < int(num_colors):
        cubes.sort(key=lambda cube: cube.shape[0], reverse=True)
        largest_cube = cubes.pop(0)
        left, right = split_cube(largest_cube)
        cubes.append(left)
        cubes.append(right)
    
    rgb_colors = [tuple(cube.mean(axis=0).astype(int)) for cube in cubes]
    palette = list('#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in rgb_colors)
    return palette


def octree_quantization(image_path, num_colors):
    pixels = image_to_pixels(image_path)
    
    octree = OctreeQuantizer()
    for pixel in pixels:
        octree.add_color(Color(*pixel))
    palette = octree.make_palette(int(num_colors))

    rgb_colors = [(color.red, color.blue, color.green) for color in palette]
    palette = list('#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in rgb_colors)
    return palette
