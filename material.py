from RayClass import Ray
#import hittable
import helloray
import numpy as np


def near_zero(vector: np.array):
    s = 1e-8
    if vector[0] < s and vector[1] < s and vector[2] < s:
        return True
    else:
        return False


def reflect(v, n):
    # Gives reflected ray given  input v and normal n
    return v - 2*v.dot(n)*n


class myattenuation:
    def __init__(self, mylist=None):
        if mylist is None:
            mylist = [0, 0, 0]
        self.atten = np.array(mylist)

    def set_as_other(self, other):
        self.atten = other.atten


class material:
    def scatter(self, r_in: Ray, rec, attenuation, scattered: Ray):
        pass


class lambertian(material):
    def __init__(self, a: np.array):
        self.albedo = a

    def scatter(self, r_in: Ray, rec, attenuation, scattered: Ray):
        # scatters in normal diffuse way
        scatter_direction = rec.normal + helloray.random_unit_vector()
        if near_zero(scatter_direction):
            scatter_direction = rec.normal
        scattered.set_as_alt_ray(Ray(rec.p, scatter_direction))
        attenuation.atten = self.albedo
        return True


class metal(material):
    def __init__(self, a: np.array):
        self.albedo = a

    def scatter(self, r_in: Ray, rec, attenuation, scattered: Ray):
        # Get reflected ray direction
        reflected = reflect(helloray.unit_vector(r_in.direction()), rec.normal)
        # Set scattered to be the ray we want
        scattered.set_as_alt_ray(Ray(rec.p, reflected))
        # TODO: attenuation not getting albedo value
        attenuation.atten = self.albedo
        return scattered.direction().dot(rec.normal) > 0


