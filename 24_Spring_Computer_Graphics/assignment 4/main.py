from PIL import Image
from ray import Ray
from color import Color
from pyglet.math import Vec3
from shapes import *
from materials import *
import math

objects = []
lights = []
MAX_DEPTH = 4

def TraceRay(ray, depth=1, n=1.0):
    if depth > MAX_DEPTH:
        return Color(0, 0, 0, 255)
    hit = CheckIntersectionAll(ray)
    color = Color(0, 0, 0, 255)
    if hit != None:
        #color = ambient * hit.getDiffuseColor()
        for light in lights:
            shadowRay = Ray(hit.position + hit.getNormal() * 0.0001, light.position - hit.position)
            hit2 = CheckIntersectionAllShadow(shadowRay)
            if hit2 != None:
                if abs(hit2.getDist() - light.intersect(shadowRay).getDist()) < 0.001:
                    color += LocalShade(ray, hit, light)
            #color += hit.color
        
        if hit.material != None and hit.material.reflectiveness > 0:
            dirReflect = ray.direction - hit.getNormal() * 2 * ray.direction.dot(hit.getNormal())
            if n == 1.0:    # ray from air
                reflectRay = Ray(hit.position + hit.getNormal() * 0.0001, dirReflect)
            else:   # ray from material
                reflectRay = Ray(hit.position - hit.getNormal() * 0.0001, dirReflect)
            color += TraceRay(reflectRay, depth + 1) * hit.material.reflectiveness

        if hit.material != None and hit.material.refractiveness > 0:
            ior = hit.material.ior
            n1 = n
            n2 = ior
            if n == ior:
                n2 = 1.0
            if n1 == 1.0: # from air to material
                cosTheta = -ray.direction.dot(hit.getNormal())
                sinThetaRefr = n1 / n2 * math.sqrt(1 - cosTheta ** 2)
                if sinThetaRefr > 1.0:
                    return color
                cosThetaRefr = math.sqrt(1 - sinThetaRefr ** 2)
                dirRefract = ray.direction * (n1 / n2) + hit.getNormal() * (n1 / n2 * cosTheta - cosThetaRefr)
                refractRay = Ray(hit.position - hit.getNormal() * 0.0001, dirRefract)
            else:   # from material to air
                cosTheta = ray.direction.dot(hit.getNormal())
                sinThetaRefr = n1 / n2 * math.sqrt(1 - cosTheta ** 2)
                if sinThetaRefr > 1.0:
                    return color
                cosThetaRefr = math.sqrt(1 - sinThetaRefr ** 2)
                dirRefract = ray.direction * (n1 / n2) - hit.getNormal() * (n1 / n2 * cosTheta + cosThetaRefr)
                refractRay = Ray(hit.position + hit.getNormal() * 0.0001, dirRefract)
            color += TraceRay(refractRay, depth + 1, n2) * hit.material.refractiveness


    return color

def LocalShade(ray, hit, light):

    k_ambient = 0.0
    k_diffuse = 0.5
    k_specular = 0.5
    shininess = 32
    color = hit.color

    if hit.material != None:
        k_ambient = hit.material.ambient
        k_diffuse = hit.material.diffuse
        k_specular = hit.material.specular
        shininess = hit.material.shininess
        color = hit.material.color

    ambient = k_ambient

    dirToLight = light.position - hit.position
    lightDir = dirToLight.normalize()
    hitNormal = hit.getNormal()
    diffuse = max(0, lightDir.dot(hitNormal)) * k_diffuse

    viewDir = ray.direction.normalize()
    reflectDir = (hitNormal * 2 * lightDir.dot(hitNormal) - lightDir).normalize()
    specular = max(0, viewDir.dot(reflectDir)) ** shininess * k_specular

    return color * (ambient + diffuse + specular) * light.color * light.intensity / (hit.position.distance(light.position) ** 2)

def CheckIntersectionAll(ray):
    distMin = float('inf')
    hitMin = None
    for obj in objects + lights:
        hit = obj.intersect(ray)
        if hit == None:
            continue
        d = hit.getDist()
        if d < distMin:
            distMin = d
            hitMin = hit
    return hitMin

def CheckIntersectionAllShadow(ray):
    distMin = float('inf')
    hitMin = None
    for obj in objects + lights:
        hit = obj.intersect(ray)
        if hit == None or hit.material.__class__.__name__ == 'Glass':
            continue
        d = hit.getDist()
        if d < distMin:
            distMin = d
            hitMin = hit
    return hitMin
   

def AddShapes():
    # platform
    objects.append(Cube(Vec3(0, -10, 5), Color(255, 255, 255, 255), Vec3(20, 1, 20), Plastic(Color(255, 255, 255, 255))))
    # back wall
    objects.append(Cube(Vec3(0, 0, 15), Color(255, 255, 255, 255), Vec3(20, 20, 1), Plastic(Color(255, 255, 255, 255))))
    # left wall
    objects.append(Cube(Vec3(-10, 0, 5), Color(255, 0, 0, 255), Vec3(1, 20, 20), Plastic(Color(255, 0, 0, 255))))
    # right wall
    objects.append(Cube(Vec3(10, 0, 5), Color(0, 0, 255, 255), Vec3(1, 20, 20), Plastic(Color(0, 0, 255, 255))))
    # ceiling
    objects.append(Cube(Vec3(0, 10, 5), Color(255, 255, 255, 255), Vec3(20, 1, 20), Plastic(Color(255, 255, 255, 255))))
    # front wall
    objects.append(Cube(Vec3(0, 0, -5), Color(255, 255, 255, 255), Vec3(20, 20, 1), Plastic(Color(255, 255, 255, 255))))


    sphere = Sphere(Vec3(-4, 4, 9), Color(155, 50, 0, 255), 3, Plastic(Color(155, 50, 0, 255)))
    objects.append(sphere)
    sphere = Sphere(Vec3(6.5, -6.5, 11.5), Color(100, 100, 100, 255), 3, Metal(Color(100, 100, 100, 255)))
    objects.append(sphere)
    sphere = Sphere(Vec3(-4, -3, 7), Color(0, 0, 0, 255), 3, Glass())
    objects.append(sphere)
    cube = Cube(Vec3(-3, -6, 11), Color(0, 255, 0, 255), Vec3(3, 3, 3), Plastic(Color(0, 255, 0, 255)))
    objects.append(cube)
    
    

def AddLights():
    light = SphereLight(Vec3(1, 7, -2.2), Color(255, 255, 255, 255), 1, 500)
    lights.append(light)
    

# this codes are for ray tracing
if __name__ ==  '__main__':

    width = 400
    height = 300
    fov = 90
    img = Image.new('RGB', (width, height), color = 'black')
    
    AddShapes()
    AddLights()

    for y in range(0, height):
        for x in range(0, width):
            ray = Ray(Vec3(0, 0, 0), Vec3(x - width // 2 + 0.1, height // 2 - y + 0.1, width / (2 * math.tan(fov / 2))))
            color1 = TraceRay(ray)
            ray = Ray(Vec3(0, 0, 0), Vec3(x - width // 2 - 0.1, height // 2 - y - 0.1, width / (2 * math.tan(fov / 2))))
            color2 = TraceRay(ray)
            ray = Ray(Vec3(0, 0, 0), Vec3(x - width // 2 + 0.1, height // 2 - y - 0.1, width / (2 * math.tan(fov / 2))))
            color3 = TraceRay(ray)
            ray = Ray(Vec3(0, 0, 0), Vec3(x - width // 2 - 0.1, height // 2 - y + 0.1, width / (2 * math.tan(fov / 2))))
            color4 = TraceRay(ray)
            color = ((color1 + color2 + color3 + color4) / 4).int_color()
            img.putpixel((x, y), (color.r, color.g, color.b))

    img.save('output.png')