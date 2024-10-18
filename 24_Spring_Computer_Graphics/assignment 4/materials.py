from color import Color

class Material:
    def __init__(self, color, ambient, diffuse, specular, shininess, reflectiveness=0, refractiveness=0, ior=1.5):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflectiveness = reflectiveness
        self.refractiveness = refractiveness
        self.ior = ior

class Plastic(Material):
    def __init__(self, color):
        super().__init__(color, 0.1, 0.6, 0.3, 32, 0, 0, 1.5)

class Metal(Material):
    def __init__(self, color):
        super().__init__(color, 0.1, 0.5, 0.4, 51.2, 0.5, 0, 2.5)

class Glass(Material):
    def __init__(self):
        super().__init__(Color(0, 0, 0, 255), 0.0, 0.0, 0.0, 0, 0.1, 0.9, 1.1)

    