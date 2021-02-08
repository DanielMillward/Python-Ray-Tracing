import numpy as np


class Ray:

    def __init__(self, origin, direction):
        """

        :param origin: numpy array of origin of ray
        :param direction: numpy array of ray direction
        """
        self.orig = origin
        self.dir = direction

    def origin(self):
        return self.orig

    def direction(self):
        return self.dir

    def at(self, t):
        """
        Given distance t, gives point away from origin t away along ray
        :return: point
        """
        return self.orig + t*self.dir

    def set_as_alt_ray(self, other):
        self.orig = other.orig
        self.dir = other.dir
