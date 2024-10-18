from pyglet.math import Vec3
from color import Color

class Shape:
    def __init__(self, position, color, material=None):
        self.position = position
        self.color = color
        self.material = material

    def intersect(self, ray):
        pass

    def calculate_normal(self, position):
        pass

class Hit:
    def __init__(self):
        self.t = 0
        self.position = Vec3(0, 0, 0)
        self.normal = Vec3(0, 0, 0)
        self.color = Color(0, 0, 0, 255)
        self.material = None

    def getDist(self):
        return self.t

    def getNormal(self):
        return self.normal

    def getDiffuseColor(self):
        return self.color
    
class Light:
    def __init__(self, position, color, intensity):
        self.position = position
        self.color = color
        self.intensity = intensity

class Sphere(Shape):
    def __init__(self, position, color, radius, material=None):
        super().__init__(position, color, material)
        self.radius = radius

    def intersect(self, ray):
        oc = ray.origin - self.position
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None
        else:
            t = (-b - discriminant ** 0.5) / (2.0 * a)
            hit = Hit()
            if t < 0:
                return None
            hit.t = t
            hit.position = ray.point_at_parameter(t)
            hit.normal = (hit.position - self.position) / self.radius
            hit.color = self.color
            hit.material = self.material
            return hit
        
    def calculate_normal(self, position):
        return (position - self.position) / self.radius
    
class SphereLight(Sphere):
    def __init__(self, position, color, radius, intensity):
        super().__init__(position, color, radius)
        self.intensity = intensity

    def intersect(self, ray):
        hit = super().intersect(ray)
        if hit == None:
            return None
        hit.color = self.color
        return hit


class Cube(Shape):
    def __init__(self, position, color, size, material=None):
        super().__init__(position, color, material)
        self.size = size

    def intersect(self, ray):
        t_min = float('-inf')
        t_max = float('inf')
        for i in range(3):
            t1 = float('-inf')
            t2 = float('inf')
            if ray.direction[i] == 0:
                if ray.origin[i] < self.position[i] - self.size[i] / 2 or ray.origin[i] > self.position[i] + self.size[i] / 2:
                    return None
            else:
                t1 = (self.position[i] - self.size[i] / 2 - ray.origin[i]) / ray.direction[i]
                t2 = (self.position[i] + self.size[i] / 2 - ray.origin[i]) / ray.direction[i]
            if t1 > t2:
                t1, t2 = t2, t1
            if t1 > t_min:
                t_min = t1
            if t2 < t_max:
                t_max = t2
            if t_min > t_max:
                return None
        t = t_min if t_min > 0 else t_max
        hit = Hit()
        if t < 0:
            return None
        hit.t = t
        hit.position = ray.point_at_parameter(t)
        hit.normal = self.calculate_normal(hit.position)
        hit.color = self.color
        hit.material = self.material
        return hit
    
    def calculate_normal(self, position):
        normal = Vec3(0, 0, 0)
        for i in range(3):
            if position[i] < self.position[i] - self.size[i] / 2 + 0.01:
                normal[i] = -1
            elif position[i] > self.position[i] + self.size[i] / 2 - 0.01:
                normal[i] = 1
        return normal
        
