class Color():
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b, self.a + other.a)
    
    def __sub__(self, other):
        return Color(self.r - other.r, self.g - other.g, self.b - other.b, self.a - other.a)
    
    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return Color(self.r * other, self.g * other, self.b * other, self.a * other)
        return Color(self.r * other.r / 255, self.g * other.g / 255, self.b * other.b / 255, self.a * other.a / 255)
    
    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return Color(self.r / other, self.g / other, self.b / other, self.a / other)
        return Color(self.r / other.r, self.g / other.g, self.b / other.b, self.a / other.a)

    def __str__(self):
        return f'Color({self.r}, {self.g}, {self.b}, {self.a})'
    
    def int_color(self):
        return Color(int(self.r), int(self.g), int(self.b), int(self.a))