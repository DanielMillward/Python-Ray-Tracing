from RayClass import Ray
# import material

class HitRecord:
    def __init__(self, p=0, normal=0, t=0, front_face=0, mat_ptr=0):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face
        self.mat_ptr = mat_ptr

    def set_face_normal(self, r: Ray, outward_normal):
        self.front_face = r.direction().dot(outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal

    def set_as_other_hitrecord(self, other):
        self.p = other.p
        self.normal = other.normal
        self.t = other.t
        self.front_face = other.front_face
        self.mat_ptr = other.mat_ptr


class hittable:
    def hit(self, r: Ray, t_min, t_max, rec: HitRecord):
        pass


class hittable_list(hittable):
    def __init__(self, objects=[]):
        self.objects = objects

    def append(self, object):
        self.objects.append(object)

    def hit(self, r: Ray, t_min, t_max, rec: HitRecord):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max

        for object in self.objects: # for every sphere
            # if sphere is hit
            if object.hit(r, t_min, closest_so_far, temp_rec):
                #Change hittable list
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.set_as_other_hitrecord(temp_rec)

        return hit_anything
