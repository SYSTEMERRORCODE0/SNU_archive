import pyglet
from pyglet import window, app, shapes
from pyglet.math import Mat4, Vec3, Vec4
import math
from pyglet.gl import *

import shader

class CustomGroup(pyglet.graphics.Group):
    '''
    To draw multiple 3D shapes in Pyglet, you should make a group for an object.
    '''
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(order)

        '''
        Create shader program for each shape
        '''
        self.shader_program = shader.create_program(
            shader.vertex_source_default, shader.fragment_source_default
        )

        self.transform_mat = transform_mat
        self.indexed_vertices_list = None
        self.shader_program.use()

    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.order == other.order and
                self.parent == other.parent)
    
    def __hash__(self):
        return hash((self.order))
    
'''
same as CustomGroup but it has a list of points, lines, triangles
'''
class PointGroup(CustomGroup):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(transform_mat, order)
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

class LineGroup(CustomGroup):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(transform_mat, order)
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

class TriangleGroup(CustomGroup):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(transform_mat, order)
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

class DerivedLineGroup(CustomGroup):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(transform_mat, order)
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()
    
class DerivedSurfaceGroup(CustomGroup):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(transform_mat, order)
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

class DerivedSubdivisionLineGroup(CustomGroup):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(transform_mat, order)
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

class DerivedSubdivisionSurfaceGroup(CustomGroup):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(transform_mat, order)
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

class NullGroup(CustomGroup):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(transform_mat, order)
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

class Cube:
    '''
    default structure of cube
    '''
    def __init__(self, scale=1.0):
        self.vertices = [-0.5, -0.5, 0.5,
            0.5, -0.5, 0.5,
            0.5, 0.5, 0.5,
            -0.5, 0.5, 0.5,
            -0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5,0.5,-0.5,
            -0.5,0.5,-0.5]
        self.vertices = [scale[idx%3] * x for idx, x in enumerate(self.vertices)]
    
        self.indices = [0, 1, 2, 2, 3, 0,
                    4, 7, 6, 6, 5, 4,
                    4, 5, 1, 1, 0, 4,
                    6, 7, 3, 3, 2, 6,
                    5, 6, 2, 2, 1, 5,
                    7, 4, 0, 0, 3, 7]
    
        self.colors = (255, 255, 255, 255,
                       255, 255, 255, 255,
                       255, 255, 255, 255,
                       255, 255, 255, 255,
                       255, 255, 255, 255,
                       255, 255, 255, 255,
                       255, 255, 255, 255,
                       255, 255, 255, 255)
        
class Sphere:
    '''
    default structure of sphere
    '''
    def __init__(self, stacks, slices, scale=1.0):
        num_triangles = 2 * slices * (stacks - 1)

        self.vertices = []
        self.indices = []
        self.colors = ()

        for i in range(stacks):
            phi0 = 0.5 * math.pi - (i * math.pi) / stacks
            phi1 = 0.5 * math.pi - ((i + 1) * math.pi) / stacks
            coord_v0 = 1.0 - float(i) / stacks
            coord_v1 = 1.0 - float(i + 1) / stacks

            y0 = scale * math.sin(phi0)
            r0 = scale * math.cos(phi0)
            y1 = scale * math.sin(phi1)
            r1 = scale * math.cos(phi1)
            y2 = y1
            y3 = y0

            for j in range(slices):
                theta0 = (j * 2 * math.pi) / slices
                theta1 = ((j + 1) * 2 * math.pi) / slices
                coord_u0 = float(j) / slices
                coord_u1 = float(j + 1) / slices

                x0 = r0 * math.cos(theta0)
                z0 = r0 * math.sin(-theta0)
                u0 = coord_u0
                v0 = coord_v0
                x1 = r1 * math.cos(theta0)
                z1 = r1 * math.sin(-theta0)
                u1 = coord_u0
                v1 = coord_v1
                x2 = r1 * math.cos(theta1)
                z2 = r1 * math.sin(-theta1)
                u2 = coord_u1
                v2 = coord_v1
                x3 = r0 * math.cos(theta1)
                z3 = r0 * math.sin(-theta1)
                u3 = coord_u1
                v3 = coord_v0

                if (i != stacks - 1):
                    self.vertices.append(x0)
                    self.vertices.append(y0)
                    self.vertices.append(z0)

                    self.vertices.append(x1)
                    self.vertices.append(y1)
                    self.vertices.append(z1)

                    self.vertices.append(x2)
                    self.vertices.append(y2)
                    self.vertices.append(z2)
                    
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                
                if (i != 0):
                    self.vertices.append(x2)
                    self.vertices.append(y2)
                    self.vertices.append(z2)

                    self.vertices.append(x3)
                    self.vertices.append(y3)
                    self.vertices.append(z3)

                    self.vertices.append(x0)
                    self.vertices.append(y0)
                    self.vertices.append(z0)
                    
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)

        for i in range(num_triangles*3):
            self.indices.append(i)

class PointSet:

    def __init__(self, positions):
        self.positions = positions

        self.vertices = []
        self.indices = []
        self.colors = []

        for position in positions:
            self.vertices.append(position.x)
            self.vertices.append(position.y)
            self.vertices.append(position.z)
            self.colors += (255, 0, 0, 255)

        for i in range(len(positions)):
            self.indices.append(i)
        
class LineSet:
    
    def __init__(self, positions, pairs):
        self.positions = positions
        self.pairs = pairs

        self.vertices = []
        self.indices = []
        self.colors = []

        for position in positions:
            self.vertices.append(position.x)
            self.vertices.append(position.y)
            self.vertices.append(position.z)
            self.colors += (0, 255, 0, 255)

        for pair in pairs:
            self.indices.append(pair[0])
            self.indices.append(pair[1])

class TriangleSet:
    def __init__(self, positions, triangles):
        self.positions = positions
        self.triangles = triangles

        self.vertices = []
        self.indices = []
        self.colors = []

        for position in positions:
            self.vertices.append(position.x)
            self.vertices.append(position.y)
            self.vertices.append(position.z)
            self.colors += (0, 0, 255, 50)

        for triangle in triangles:
            self.indices.append(triangle[0])
            self.indices.append(triangle[1])
            self.indices.append(triangle[2])

class DerivedLine:
    def __init__(self):
        self.vertices = [0, 0, 0] * 100
        self.indices = []
        self.colors = (0, 0, 0, 150) * 100

        for i in range(0, 100):
            if i % 10 != 9:
                self.indices.append(i)
                self.indices.append(i+1)
            if i < 90:
                self.indices.append(i)
                self.indices.append(i+10)

class DerivedSurface:
    def __init__(self):
        self.vertices = [0, 0, 0] * 100
        self.indices = []
        self.colors = (157, 50, 255, 230) * 100

        for i in range(0, 90, 10):
            for j in range(0, 9):
                self.indices.append(i+j)
                self.indices.append(i+j+1)
                self.indices.append(i+j+10)
                self.indices.append(i+j+1)
                self.indices.append(i+j+11)
                self.indices.append(i+j+10)

class DerivedSubdivisionLine:
    def __init__(self, v, e, f):
        self.vertices = [0, 0, 0] * (len(v) + len(e) + len(f))

        f_num = 0
        for i in f:
            f_num += len(i)

        self.indices = [0, 0] * (2 * len(e) + f_num)
        self.colors = (0, 0, 0, 150) * (len(v) + len(e) + len(f))

class DerivedSubdivisionSurface:
    def __init__(self, v, e, f):
        self.vertices = [0, 0, 0] * (len(v) + len(e) + len(f))

        f_num = 0
        for i in f:
            f_num += len(i)

        self.indices = [0, 0, 0] * (2 * f_num)
        self.colors = (157, 50, 255, 230) * (len(v) + len(e) + len(f))