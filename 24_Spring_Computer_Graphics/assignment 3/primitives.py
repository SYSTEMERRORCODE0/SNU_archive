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

class PhongTriangleGroup(TriangleGroup):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(transform_mat, order)
        self.shader_program = shader.create_program(
            shader.vertex_source_phong, shader.fragment_source_phong
        )
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

class PhongWithTextureTriangleGroup(TriangleGroup):
    def __init__(self, transform_mat: Mat4, order, textureBaseColorFilename, textureMixedAOFilename, textureRoughnessFilename, textureSpecularFilename):
        super().__init__(transform_mat, order)
        self.shader_program = shader.create_program(
            shader.vertex_source_phong_texture, shader.fragment_source_phong_texture
        )

        self.textureBaseColorFilename = textureBaseColorFilename
        self.textureMixedAOFilename = textureMixedAOFilename
        self.textureRoughnessFilename = textureRoughnessFilename
        self.textureSpecularFilename = textureSpecularFilename

        self.textureBaseColor = pyglet.image.load(self.textureBaseColorFilename).get_texture()
        self.textureMixedAO = pyglet.image.load(self.textureMixedAOFilename).get_texture()
        self.textureRoughness = pyglet.image.load(self.textureRoughnessFilename).get_texture()
        self.textureSpecular = pyglet.image.load(self.textureSpecularFilename).get_texture()
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureBaseColor.id)
        self.shader_program['textureBaseColor'] = 0

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.textureMixedAO.id)
        self.shader_program['textureMixedAO'] = 1

        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.textureRoughness.id)
        self.shader_program['textureRoughness'] = 2

        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.textureSpecular.id)
        self.shader_program['textureSpecular'] = 3

    def unset_state(self):
        self.shader_program.stop()

class PhongWithTextureWithNormalTriangleGroup(TriangleGroup):
    def __init__(self, transform_mat: Mat4, order, textureBaseColorFilename, textureMixedAOFilename, textureRoughnessFilename, textureSpecularFilename, textureNormalFilename):
        super().__init__(transform_mat, order)
        self.shader_program = shader.create_program(
            shader.vertex_source_phong_texture_normal, shader.fragment_source_phong_texture_normal
        )

        self.textureBaseColorFilename = textureBaseColorFilename
        self.textureMixedAOFilename = textureMixedAOFilename
        self.textureRoughnessFilename = textureRoughnessFilename
        self.textureSpecularFilename = textureSpecularFilename
        self.textureNormalFilename = textureNormalFilename

        self.textureBaseColor = pyglet.image.load(self.textureBaseColorFilename).get_texture()
        self.textureMixedAO = pyglet.image.load(self.textureMixedAOFilename).get_texture()
        self.textureRoughness = pyglet.image.load(self.textureRoughnessFilename).get_texture()
        self.textureSpecular = pyglet.image.load(self.textureSpecularFilename).get_texture()
        self.textureNormal = pyglet.image.load(self.textureNormalFilename).get_texture()
            
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureBaseColor.id)
        self.shader_program['textureBaseColor'] = 0

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.textureMixedAO.id)
        self.shader_program['textureMixedAO'] = 1

        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.textureRoughness.id)
        self.shader_program['textureRoughness'] = 2

        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.textureSpecular.id)
        self.shader_program['textureSpecular'] = 3

        glActiveTexture(GL_TEXTURE4)
        glBindTexture(GL_TEXTURE_2D, self.textureNormal.id)
        self.shader_program['textureNormal'] = 4

    def unset_state(self):
        self.shader_program.stop()


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
    def __init__(self, positions, triangles, triangles_texture, triangles_normal, textures, normals):
        self.positions = positions
        self.triangles = triangles

        self.vertices = []
        self.indices = []
        self.colors = []
        self.normals = []
        self.textures = []
        self.v_to_vt = {}
        self.v_to_vn = {}

        self.v_to_deltaPos = {}
        self.v_to_deltaUV = {}

        self.deltaPos1 = []
        self.deltaPos2 = []
        self.deltaUV1 = []
        self.deltaUV2 = []

        for position in positions:
            self.vertices.append(position.x)
            self.vertices.append(position.y)
            self.vertices.append(position.z)
            self.colors += (150, 150, 150, 255)

        for i in range(len(triangles_texture)):
            if triangles[i][0] not in self.v_to_vt:
                self.v_to_vt[triangles[i][0]] = triangles_texture[i][0]
            elif triangles_texture[i][0] != self.v_to_vt[triangles[i][0]]:
                self.add_pseudo_point(triangles[i][0])
                triangles[i][0] = len(self.vertices) // 3 - 1
                self.v_to_vt[triangles[i][0]] = triangles_texture[i][0]
                self.v_to_vn[triangles[i][0]] = triangles_normal[i][0]

            if triangles[i][1] not in self.v_to_vt:
                self.v_to_vt[triangles[i][1]] = triangles_texture[i][1]
            elif triangles_texture[i][1] != self.v_to_vt[triangles[i][1]]:
                self.add_pseudo_point(triangles[i][1])
                triangles[i][1] = len(self.vertices) // 3 - 1
                self.v_to_vt[triangles[i][1]] = triangles_texture[i][1]
                self.v_to_vn[triangles[i][1]] = triangles_normal[i][1]

            if triangles[i][2] not in self.v_to_vt:
                self.v_to_vt[triangles[i][2]] = triangles_texture[i][2]
            elif triangles_texture[i][2] != self.v_to_vt[triangles[i][2]]:
                self.add_pseudo_point(triangles[i][2])
                triangles[i][2] = len(self.vertices) // 3 - 1
                self.v_to_vt[triangles[i][2]] = triangles_texture[i][2]
                self.v_to_vn[triangles[i][2]] = triangles_normal[i][2]

        for i in range(len(triangles_normal)):
            if triangles[i][0] not in self.v_to_vn:
                self.v_to_vn[triangles[i][0]] = triangles_normal[i][0]
            elif triangles_normal[i][0] != self.v_to_vn[triangles[i][0]]:
                self.add_pseudo_point(triangles[i][0])
                triangles[i][0] = len(self.vertices) // 3 - 1
                self.v_to_vt[triangles[i][0]] = triangles_texture[i][0]
                self.v_to_vn[triangles[i][0]] = triangles_normal[i][0]

            if triangles[i][1] not in self.v_to_vn:
                self.v_to_vn[triangles[i][1]] = triangles_normal[i][1]
            elif triangles_normal[i][1] != self.v_to_vn[triangles[i][1]]:
                self.add_pseudo_point(triangles[i][1])
                triangles[i][1] = len(self.vertices) // 3 - 1
                self.v_to_vt[triangles[i][1]] = triangles_texture[i][1]
                self.v_to_vn[triangles[i][1]] = triangles_normal[i][1]

            if triangles[i][2] not in self.v_to_vn:
                self.v_to_vn[triangles[i][2]] = triangles_normal[i][2]
            elif triangles_normal[i][2] != self.v_to_vn[triangles[i][2]]:
                self.add_pseudo_point(triangles[i][2])
                triangles[i][2] = len(self.vertices) // 3 - 1
                self.v_to_vt[triangles[i][2]] = triangles_texture[i][2]
                self.v_to_vn[triangles[i][2]] = triangles_normal[i][2]

        for i in range(len(self.vertices) // 3):
            self.textures.append(textures[self.v_to_vt[i]].x)
            self.textures.append(textures[self.v_to_vt[i]].y)
            self.normals.append(normals[self.v_to_vn[i]].x)
            self.normals.append(normals[self.v_to_vn[i]].y)
            self.normals.append(normals[self.v_to_vn[i]].z)

        for triangle in triangles:
            self.indices.append(triangle[0])
            self.indices.append(triangle[1])
            self.indices.append(triangle[2])
            
            if triangle[0] not in self.v_to_deltaPos:
                self.v_to_deltaPos[triangle[0]] = [Vec3(round(self.vertices[triangle[1]*3] - self.vertices[triangle[0]*3],4), 
                                                        round(self.vertices[triangle[1]*3+1] - self.vertices[triangle[0]*3+1],4), 
                                                        round(self.vertices[triangle[1]*3+2] - self.vertices[triangle[0]*3+2],4)), 
                                                Vec3(round(self.vertices[triangle[2]*3] - self.vertices[triangle[0]*3],4), 
                                                        round(self.vertices[triangle[2]*3+1] - self.vertices[triangle[0]*3+1],4), 
                                                        round(self.vertices[triangle[2]*3+2] - self.vertices[triangle[0]*3+2],4))]
            if triangle[1] not in self.v_to_deltaPos:
                self.v_to_deltaPos[triangle[1]] = [Vec3(round(self.vertices[triangle[2]*3] - self.vertices[triangle[1]*3],4), 
                                                        round(self.vertices[triangle[2]*3+1] - self.vertices[triangle[1]*3+1],4), 
                                                        round(self.vertices[triangle[2]*3+2] - self.vertices[triangle[1]*3+2],4)), 
                                                Vec3(round(self.vertices[triangle[0]*3] - self.vertices[triangle[1]*3],4), 
                                                        round(self.vertices[triangle[0]*3+1] - self.vertices[triangle[1]*3+1],4), 
                                                        round(self.vertices[triangle[0]*3+2] - self.vertices[triangle[1]*3+2],4))]
            if triangle[2] not in self.v_to_deltaPos:
                self.v_to_deltaPos[triangle[2]] = [Vec3(round(self.vertices[triangle[0]*3] - self.vertices[triangle[2]*3],4), 
                                                        round(self.vertices[triangle[0]*3+1] - self.vertices[triangle[2]*3+1],4), 
                                                        round(self.vertices[triangle[0]*3+2] - self.vertices[triangle[2]*3+2],4)), 
                                                Vec3(round(self.vertices[triangle[1]*3] - self.vertices[triangle[2]*3],4), 
                                                        round(self.vertices[triangle[1]*3+1] - self.vertices[triangle[2]*3+1],4), 
                                                        round(self.vertices[triangle[1]*3+2] - self.vertices[triangle[2]*3+2],4))]

            if self.v_to_vt[triangle[0]] not in self.v_to_deltaUV:    
                self.v_to_deltaUV[self.v_to_vt[triangle[0]]] = [Vec3(round(self.textures[self.v_to_vt[triangle[1]]*2] - self.textures[self.v_to_vt[triangle[0]]*2],4), 
                                                                    round(self.textures[self.v_to_vt[triangle[1]]*2+1] - self.textures[self.v_to_vt[triangle[0]]*2+1],4),
                                                                    0),
                                                                Vec3(round(self.textures[self.v_to_vt[triangle[2]]*2] - self.textures[self.v_to_vt[triangle[0]]*2],4),
                                                                    round(self.textures[self.v_to_vt[triangle[2]]*2+1] - self.textures[self.v_to_vt[triangle[0]]*2+1],4),
                                                                    0)]
            if self.v_to_vt[triangle[1]] not in self.v_to_deltaUV:
                self.v_to_deltaUV[self.v_to_vt[triangle[1]]] = [Vec3(round(self.textures[self.v_to_vt[triangle[2]]*2] - self.textures[self.v_to_vt[triangle[1]]*2],4),
                                                                    round(self.textures[self.v_to_vt[triangle[2]]*2+1] - self.textures[self.v_to_vt[triangle[1]]*2+1],4),
                                                                    0),
                                                                Vec3(round(self.textures[self.v_to_vt[triangle[0]]*2] - self.textures[self.v_to_vt[triangle[1]]*2],4),
                                                                    round(self.textures[self.v_to_vt[triangle[0]]*2+1] - self.textures[self.v_to_vt[triangle[1]]*2+1],4),
                                                                    0)]
            if self.v_to_vt[triangle[2]] not in self.v_to_deltaUV:
                self.v_to_deltaUV[self.v_to_vt[triangle[2]]] = [Vec3(round(self.textures[self.v_to_vt[triangle[0]]*2] - self.textures[self.v_to_vt[triangle[2]]*2],4),
                                                                    round(self.textures[self.v_to_vt[triangle[0]]*2+1] - self.textures[self.v_to_vt[triangle[2]]*2+1],4),
                                                                    0),
                                                                Vec3(round(self.textures[self.v_to_vt[triangle[1]]*2] - self.textures[self.v_to_vt[triangle[2]]*2],4),
                                                                    round(self.textures[self.v_to_vt[triangle[1]]*2+1] - self.textures[self.v_to_vt[triangle[2]]*2+1],4),
                                                                    0)]
            
        for i in range(len(self.vertices) // 3):
            self.deltaPos1.append(self.v_to_deltaPos[i][0].x)
            self.deltaPos1.append(self.v_to_deltaPos[i][0].y)
            self.deltaPos1.append(self.v_to_deltaPos[i][0].z)
            self.deltaPos2.append(self.v_to_deltaPos[i][1].x)
            self.deltaPos2.append(self.v_to_deltaPos[i][1].y)
            self.deltaPos2.append(self.v_to_deltaPos[i][1].z)
            self.deltaUV1.append(self.v_to_deltaUV[self.v_to_vt[i]][0].x)
            self.deltaUV1.append(self.v_to_deltaUV[self.v_to_vt[i]][0].y)
            self.deltaUV2.append(self.v_to_deltaUV[self.v_to_vt[i]][1].x)
            self.deltaUV2.append(self.v_to_deltaUV[self.v_to_vt[i]][1].y)
        

    def add_pseudo_point(self, n):
        # add a new vertex (with the same position) to the list
        self.vertices.append(self.positions[n].x)
        self.vertices.append(self.positions[n].y)
        self.vertices.append(self.positions[n].z)
        self.colors += (150, 150, 150, 255)

         
