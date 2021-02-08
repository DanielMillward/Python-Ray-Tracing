import math
import random
import numpy as np
from RayClass import Ray
import hittable
from Sphere import sphere
from camera import camera
import material
import depthcounter

# v1.magnitude()
# v1.dot(v2) for dot,
# dot(v2)
# cross(v2) scalar
# angle(v2)
# p1 = Point(2,0,2)

aspect_ratio = 1
image_width = 250
image_height = math.floor(image_width / aspect_ratio)
samples_per_pixel = 5  # 100, 40
max_depth = 5  # 50, 10

viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1.0

origin = np.array([0, 0, 0])
horizontal = np.array([viewport_width, 0, 0])
vertical = np.array([0, viewport_height, 0])
lower_left_corner = origin - horizontal / 2 - vertical / 2 - np.array([0, 0, focal_length])


def random_in_unit_sphere():
    # makes a random vector of x/y/z coords between -1 and 1
    # If this is in a unit sphere (length<1), then
    # return it
    while True:
        p = np.array([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)])
        if p.dot(p) >= 1:
            continue
        return p


def random_unit_vector():
    # Instead of sampling within unit sphere,
    # Make it on the surface instead
    return unit_vector(random_in_unit_sphere())


def clamp(x, min, max):
    if x < min:
        return min
    if x > max:
        return max
    return x


def hit_sphere(center, radius, r: Ray):
    # Dot product gives a scalar. Solving quadratic
    oc = r.origin() - center
    a = r.direction().dot(r.direction())
    b = 2 * oc.dot(r.direction())
    c = oc.dot(oc) - radius * radius
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        # basically false, didn't hit sphere
        return -1.0
    else:
        # return t value of ray to hit sphere
        return -b - math.sqrt(discriminant) / (2.0 * a)


def ray_color(r, world: hittable.hittable, depth, counter: depthcounter.depthcounter):
    # returns a color and the depth number, 10 - depth
    rec = hittable.HitRecord()

    if depth <= 0:
        counter.mycounter = 0
        return np.array([0, 0, 0])
    # If we hit something in the world collection
    if world.hit(r, 0.001, np.inf, rec):
        scattered = Ray(np.array([0, 0, 0]), np.array([0, 0, 0]))
        attenuation = material.myattenuation()
        if rec.mat_ptr.scatter(r, rec, attenuation, scattered):
            counter.mycounter = depth
            return attenuation.atten * ray_color(scattered, world, depth - 1, counter)
        counter.mycounter = depth
        return np.array([0, 0, 0])
    # Some fancy trick to get nice background
    unit_direction = unit_vector(r.direction())
    t = 0.5 * (unit_direction[1] + 1.0)
    counter.mycounter = depth
    return (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])


def unit_vector(v: np.array):
    return v / np.linalg.norm(v)


def write_color(pixel_color: np.array, samples_per_pixel):
    '''
    Given color, Writes single pixel out to imagearray
    :param pixel_color: Color np.array(r,g,b)
    :return: color line and newline
    '''
    r = pixel_color[0]
    g = pixel_color[1]
    b = pixel_color[2]

    # Divide color by num of samples. Since all
    # colors are added together, just dividing works
    # Also un-gamma correct
    scale = 1 / samples_per_pixel
    r = math.sqrt(scale * r)
    g = math.sqrt(scale * g)
    b = math.sqrt(scale * b)

    stringr = str(math.floor(256 * clamp(r, 0, 0.999))) + ' '
    stringb = str(math.floor(256 * clamp(g, 0, 0.999))) + ' '
    stringg = str(math.floor(256 * clamp(b, 0, 0.999))) + '\n'
    return stringr + stringb + stringg


def write_depth(depth, samples, maxdepth):
    # gets average of depth for that pixel
    y = depth / samples
    # translate to real depth
    x = -(y - maxdepth) / maxdepth

    r = round(255 * math.sqrt(x))
    g = round(255 * math.pow(x, 3))
    if math.sin(2 * math.pi * x) >= 0:
        b = round(255 * math.sin(2 * math.pi * x))
    else:
        b = 0
    # Divide color by num of samples. Since all
    # colors are added together, just dividing works
    # Also un-gamma correct
    r = math.sqrt(r)
    g = math.sqrt(g)
    b = math.sqrt(b)

    stringr = str(math.floor(256 * clamp(r, 0, 0.999))) + ' '
    stringb = str(math.floor(256 * clamp(g, 0, 0.999))) + ' '
    stringg = str(math.floor(256 * clamp(b, 0, 0.999))) + '\n'
    return stringr + stringb + stringg


if __name__ == '__main__':

    world = hittable.hittable_list()

    material_ground = material.lambertian(np.array([0.9, 0.8, 0.0]))
    material_center = material.lambertian(np.array([0.7, 0.3, 0.3]))
    material_left = material.metal(np.array([0.8, 0.8, 0.8]))
    material_right = material.metal(np.array([0.8, 0.6, 0.2]))

    groundsphere = sphere(np.array([0.0, -100.5, -1.0]), 100.0, material_ground)
    centersphere = sphere(np.array([0.0, 1.0, -1.5]), 0.5, material_center)
    leftsphere = sphere(np.array([-0.75, 0.0, -0.65]), 0.5, material_left)  # -1
    rightsphere = sphere(np.array([1, 0.5, -1.0]), 0.5, material_right)  # 1, 1.5 is the limit

    world.append(groundsphere)
    world.append(centersphere)
    world.append(leftsphere)
    world.append(rightsphere)
    cam = camera()

    frames = 72
    for frame in range(frames):

        if frame < 36:
            leftsphere.moveball(0, -0.014)  # x val minus
            leftsphere.moveball(2, -0.01)
            rightsphere.moveball(0, 0.014)
            rightsphere.moveball(2, -0.01)
            centersphere.moveball(2, -0.01)
            centersphere.moveball(1, -0.01)
        else:
            leftsphere.moveball(0, 0.014)  # x val minus
            leftsphere.moveball(2, -0.01)
            rightsphere.moveball(0, -0.014)
            rightsphere.moveball(2, -0.01)
            centersphere.moveball(2, -0.01)
            centersphere.moveball(1, 0.01)

        #otherreader = open('raytracenum.ppm', 'w')
        reader = open('vid' + str(frame + 1) + '.ppm', 'w')
        reader.write("P3\n" + str(image_width) + ' ' + str(image_height) + '\n255\n')
        #otherreader.write("P3\n" + str(image_width) + ' ' + str(image_height) + '\n255\n')
        j = image_height - 1
        for x in range(j, -1, -1):
            print("\rScanlines remaining: " + str(x) + ',' + str(frame))
            for y in range(image_width):
                # For every pixel
                totalpixelcounter = 0
                pixel_color = np.array([0.0, 0.0, 0.0])
                # For every sample
                for s in range(samples_per_pixel):
                    # pick a random spot in pixel, get percent over
                    u = (y + random.random()) / (image_width - 1)
                    v = (x + random.random()) / (image_height - 1)
                    # Get the ray to that position
                    r = cam.get_ray(u, v)
                    # get the color from there
                    subcounter = depthcounter.depthcounter()
                    pixel_color += ray_color(r, world, max_depth, subcounter)
                    #totalpixelcounter += subcounter.mycounter
                # Writing color to file, adjusts for sampling multiplying
                colorstring = write_color(pixel_color, samples_per_pixel)
                reader.write(colorstring)
                #depthstring = write_depth(totalpixelcounter, samples_per_pixel, max_depth)
                #otherreader.write(depthstring)

        reader.close()
        #otherreader.close()
    print("\nDone.\n")
