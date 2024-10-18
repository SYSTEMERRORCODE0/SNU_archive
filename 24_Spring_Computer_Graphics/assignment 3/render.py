import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key

from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_TRIANGLES, GL_LINES, GL_POINTS
from pyglet.math import Mat4, Vec3
from pyglet.gl import *

import shader
from primitives import *



class RenderWindow(pyglet.window.Window):
    '''
    inherits pyglet.window.Window which is the default render window of Pyglet
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        '''
        View (camera) parameters
        '''
        self.cam_eye = Vec3(15,15,15)
        self.cam_target = Vec3(0,0,0)
        self.cam_vup = Vec3(0,1,0)
        self.view_mat = None

        self.distance = (self.cam_eye - self.cam_target).mag
        '''
        Projection parameters
        '''
        self.z_near = 0.1
        self.z_far = 100000
        self.fov = 60
        self.proj_mat = None

        '''
        Camera move parameters
        '''
        self.camera_move_speed = 0.1
        self.camera_move_x = 0
        self.camera_move_y = 0
        self.camera_move_z = 0

        self.camera_mouse_move_x = 0
        self.camera_mouse_move_y = 0

        self.shapes = []
        self.setup()


        '''
        loaded object file
        '''
        self.filename = ""
        self.textureBaseColorFilename = ""
        self.textureMixedAOFilename = ""
        self.textureNormalFilename = ""
        self.textureRoughnessFilename = ""
        self.textureSpecularFilename = ""

        self.textureBaseColor = None
        self.textureMixedAO = None
        self.textureNormal = None
        self.textureRoughness = None
        self.textureSpecular = None
        
        self.rendering_group = 1

        self.animate = False

        self.shaderProgram = None

    def camera_move(self):
        normal_vec = (self.cam_target - self.cam_eye).normalize()
        right_vec = normal_vec.cross(self.cam_vup).normalize()
        up_vec = right_vec.cross(normal_vec).normalize()

        right_move_vec = right_vec * self.camera_move_x
        up_move_vec = up_vec * self.camera_move_y
        forward_move_vec = normal_vec * self.camera_move_z

        keyboard_move_vec = (right_move_vec + up_move_vec + forward_move_vec) * self.camera_move_speed

        mouse_move_vec_x = right_vec * self.camera_mouse_move_x
        mouse_move_vec_y = up_vec * self.camera_mouse_move_y

        mouse_move_vec = (mouse_move_vec_x + mouse_move_vec_y) * self.camera_move_speed
        # for not using mouse dx dy continuously
        self.camera_mouse_move_x = 0
        self.camera_mouse_move_y = 0

        self.cam_eye += keyboard_move_vec
        self.cam_target += keyboard_move_vec + mouse_move_vec

        self.cam_target = self.cam_eye + (self.cam_target - self.cam_eye).normalize() * self.distance

        self.setup()

    def setup(self) -> None:
        self.set_minimum_size(width = 400, height = 300)
        self.set_mouse_visible(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glClearColor(0.9, 0.9, 0.9, 1.0)


        # 1. Create a view matrix
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
        
        # 2. Create a projection matrix 
        self.proj_mat = Mat4.perspective_projection(
            aspect = self.width/self.height, 
            z_near=self.z_near, 
            z_far=self.z_far, 
            fov = self.fov)

    def on_draw(self) -> None:
        self.clear()
        #glPointSize(5)
        #glLineWidth(2)

        self.batch.draw()

    def update(self,dt) -> None:

        self.camera_move()

        view_proj = self.proj_mat @ self.view_mat
        for i, shape in enumerate(self.shapes):

            self.shaderProgram = self.shapes[0].shader_program
            if shape.__class__.__name__ == 'PhongTriangleGroup' or shape.__class__.__name__ == 'PhongWithTextureTriangleGroup' or shape.__class__.__name__ == 'PhongWithTextureWithNormalTriangleGroup':
                shape.shader_program['lightPos'] = Vec3(0, 10000, 10000)
                shape.shader_program['lightColor'] = Vec3(1, 1, 1)
                shape.shader_program['lightIntensity'] = 250000000.0
            shape.shader_program['view_proj'] = view_proj
            

    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect = width/height, z_near=self.z_near, z_far=self.z_far, fov = self.fov)
        return pyglet.event.EVENT_HANDLED

    def add_shape(self, transform, vertice, indices, colors, textures = None, normals = None, group = CustomGroup, mode = GL_TRIANGLES,
                  textureBaseColorFilename = None, textureMixedAOFilename = None, textureNormalFilename = None, textureRoughnessFilename = None, textureSpecularFilename = None,
                  deltaPos1 = None, deltaPos2 = None, deltaUV1 = None, deltaUV2 = None): 
        '''
        Assign a group for each shape
        '''
        if group == PhongTriangleGroup:
            shape = group(transform, len(self.shapes))
            shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, mode,
                        batch = self.batch,
                        group = shape,
                        indices = indices,
                        vertices = ('f', vertice),
                        colors = ('Bn', colors),
                        normals = ('f', normals))
        elif group == PhongWithTextureTriangleGroup:
            shape = group(transform, len(self.shapes), textureBaseColorFilename, textureMixedAOFilename, textureRoughnessFilename, textureSpecularFilename)
            shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, mode,
                        batch = self.batch,
                        group = shape,
                        indices = indices,
                        vertices = ('f', vertice),
                        textures_vertices = ('f', textures),
                        normals = ('f', normals))
        elif group == PhongWithTextureWithNormalTriangleGroup:
            shape = group(transform, len(self.shapes), textureBaseColorFilename, textureMixedAOFilename, textureRoughnessFilename, textureSpecularFilename, textureNormalFilename)
            shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, mode,
                        batch = self.batch,
                        group = shape,
                        indices = indices,
                        vertices = ('f', vertice),
                        textures_vertices = ('f', textures),
                        normals = ('f', normals),
                        deltaPos1 = ('f', deltaPos1),
                        deltaPos2 = ('f', deltaPos2),
                        deltaUV1 = ('f', deltaUV1),
                        deltaUV2 = ('f', deltaUV2))
        else:
            shape = group(transform, len(self.shapes))
            shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, mode,
                        batch = self.batch,
                        group = shape,
                        indices = indices,
                        vertices = ('f', vertice),
                        colors = ('Bn', colors))
        self.shapes.append(shape)
        
         
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    
    