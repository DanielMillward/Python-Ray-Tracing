import hittable
from RayClass import Ray
import math


class sphere(hittable.hittable):
    def __init__(self, cen, r, m):
        self.center = cen
        self.radius = r
        self.mat_ptr = m

    def hit(self, r: Ray, t_min, t_max, rec: hittable.HitRecord):
        # Solve equation of ray/sphere intersect
        oc = r.origin() - self.center
        a = r.direction().dot(r.direction())
        half_b = oc.dot(r.direction())
        c = oc.dot(oc) - self.radius * self.radius

        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return False
        sqrtd = math.sqrt(discriminant)

        # Find nearest root in acceptable range
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            # Nothing in acceptable range
            if root < t_min or t_max < root:
                return False

        # Store hit info in Hitrecord
        rec.t = root  # Quadratic answer is the t value
        rec.p = r.at(rec.t)  # Point of intersect
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        # Store material in hitrecord
        rec.mat_ptr = self.mat_ptr

        return True

    def moveball(self, dim, val):
        self.center[dim] += val
