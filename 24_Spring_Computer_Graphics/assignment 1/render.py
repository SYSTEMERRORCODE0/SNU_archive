import pyglet
import math
from pyglet import window, app, shapes
from pyglet.window import mouse,key

from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Vec3
from pyglet.gl import *

import shader
from primitives import CustomGroup



class RenderWindow(pyglet.window.Window):
    '''
    inherits pyglet.window.Window which is the default render window of Pyglet
    '''
    angle = 0
    velocity = 2
    prev_mat = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        '''
        View (camera) parameters
        '''
        self.cam_eye = Vec3(5,7,7)
        self.cam_target = Vec3(0,2,0)
        self.cam_vup = Vec3(0,1,0)
        self.view_mat = None
        '''
        Projection parameters
        '''
        self.z_near = 0.1
        self.z_far = 100
        self.fov = 60
        self.proj_mat = None

        self.shapes = []
        self.setup()

        self.animate = False

    def setup(self) -> None:
        self.set_minimum_size(width = 400, height = 300)
        self.set_mouse_visible(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

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
        self.batch.draw()

    def update(self,dt) -> None:
        view_proj = self.proj_mat @ self.view_mat

        if self.animate:
            phi = math.acos(math.sqrt(1-(1**2)*math.sin(RenderWindow.angle)**2/2**2))
            first_angle = math.pi - phi%math.pi - RenderWindow.angle%math.pi
            RenderWindow.angle += dt * RenderWindow.velocity
            phi = math.acos(math.sqrt(1-(1**2)*math.sin(RenderWindow.angle)**2/2**2))
            second_angle = math.pi - phi%math.pi - RenderWindow.angle%math.pi
        
            if second_angle > first_angle:
                second_angle -= math.pi

        for i, shape in enumerate(self.shapes):
            '''
            Update position/orientation in the scene. In the current setting, 
            shapes created later rotate faster while positions are not changed.
            '''
            if self.animate:

                # pistons
                if i < 96:
                    if i % 6 == 3: 
                        rotate_axis = Vec3(0,0,1)
                        if RenderWindow.angle % (2 * math.pi) < math.pi:
                            rotate_mat = Mat4.from_rotation(angle = second_angle - first_angle, vector = rotate_axis)
                        else:
                            rotate_mat = Mat4.from_rotation(angle = -2*RenderWindow.velocity*dt - second_angle + first_angle, vector = rotate_axis)

                        RenderWindow.prev_mat = shape.transform_mat = shape.transform_mat @ Mat4.from_translation(vector=Vec3(x=0, y=-1, z=0)) @ rotate_mat @ Mat4.from_translation(vector=Vec3(x=0, y=1, z=0))

                    if i % 6 == 4:
                        translate_cylinder_head_axis = Mat4.from_translation(vector=Vec3(x=0, y=1, z=0))
                        rotation_cylinder_head_axis_x = Mat4.from_rotation(angle=math.pi/2, vector=Vec3(x=1, y=0, z=0))
                        RenderWindow.prev_mat = shape.transform_mat = RenderWindow.prev_mat @ translate_cylinder_head_axis @ rotation_cylinder_head_axis_x

                    if i % 6 == 5:
                        translate_cylinder_head = Mat4.from_translation(vector=Vec3(x=0, y=0.25, z=0))
                        rotation_cylinder_head_x = Mat4.from_rotation(angle=-math.pi/2, vector=Vec3(x=1, y=0, z=0))
                        if RenderWindow.angle % (2 * math.pi) < math.pi:
                            rotation_cylinder_head_z = Mat4.from_rotation(angle = phi, vector=Vec3(x=0, y=0, z=1))
                        else:
                            rotation_cylinder_head_z = Mat4.from_rotation(angle = -phi, vector=Vec3(x=0, y=0, z=1))
                        shape.transform_mat = RenderWindow.prev_mat @ rotation_cylinder_head_x @ rotation_cylinder_head_z @ translate_cylinder_head

                    else:
                        rotate_angle = dt * RenderWindow.velocity
                        rotate_axis = Vec3(0,0,1)
                        rotate_mat = Mat4.from_rotation(angle = rotate_angle, vector = rotate_axis)
                        
                        shape.transform_mat = rotate_mat @ shape.transform_mat

                # axis
                elif i < 97:
                    rotate_angle = dt * RenderWindow.velocity
                    rotate_axis = Vec3(0,0,1)
                    rotate_mat = Mat4.from_rotation(angle = rotate_angle, vector = rotate_axis)
                    
                    shape.transform_mat = rotate_mat @ shape.transform_mat

                # big cog
                elif i < 118:
                    rotate_angle = dt * RenderWindow.velocity
                    rotate_axis = Vec3(0,0,1)
                    rotate_mat = Mat4.from_rotation(angle = rotate_angle, vector = rotate_axis)
                    
                    shape.transform_mat = rotate_mat @ shape.transform_mat

                # small cog
                elif i < 129:
                    if i == 118:
                        RenderWindow.prev_mat = shape.transform_mat = shape.transform_mat @ Mat4.from_rotation(angle = -2*RenderWindow.velocity*dt, vector = Vec3(0,1,0))
                    else:
                        rotation_teeth = Mat4.from_rotation(angle = 2*math.pi/10*i-2*RenderWindow.velocity*dt, vector = Vec3(0,1,0))
                        translate_teeth = Mat4.from_translation(vector=Vec3(x=0, y=0, z=1+0.3/2))
                        shape.transform_mat = RenderWindow.prev_mat @ rotation_teeth @ translate_teeth
                

                # # Example) You can control the vertices of shape.
                #shape.indexed_vertices_list.vertices[0] += 0.5 * dt

            '''
            Update view and projection matrix. There exist only one view and projection matrix 
            in the program, so we just assign the same matrices for all the shapes
            '''
            shape.shader_program['view_proj'] = view_proj
            

    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect = width/height, z_near=self.z_near, z_far=self.z_far, fov = self.fov)
        return pyglet.event.EVENT_HANDLED

    def add_shape(self, transform, vertice, indice, color):
        
        '''
        Assign a group for each shape
        '''
        shape = CustomGroup(transform, len(self.shapes))
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES,
                        batch = self.batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color))
        self.shapes.append(shape)
         
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    