import pyglet
import math
from pyglet.math import Mat4, Vec3

from render import RenderWindow
from primitives import Cube,Sphere,Cylinder
from control import Control

def add_piston(x, y, z, theta):
    crank_radius = 1
    rod_length = 2

    translate_cylinder_center_axis = Mat4.from_translation(vector=Vec3(x=x, y=y, z=z))
    rotation_cylinder_center_axis_z = Mat4.from_rotation(angle=theta, vector=Vec3(x=0, y=0, z=1))
    rotation_cylinder_center_axis_x = Mat4.from_rotation(angle=math.pi/2, vector=Vec3(x=1, y=0, z=0))
    matrix_cylinder_center_axis = translate_cylinder_center_axis @ rotation_cylinder_center_axis_z @ rotation_cylinder_center_axis_x
    cylinder_center_axis = Cylinder(30, 0.2, 0.2)

    translate_cylinder_center_pipe = Mat4.from_translation(vector=Vec3(x=0, y=crank_radius/2, z=0))
    rotation_cylinder_center_pipe_x = Mat4.from_rotation(angle=-math.pi/2, vector=Vec3(x=1, y=0, z=0))
    matrix_cylinder_center_pipe = matrix_cylinder_center_axis @ rotation_cylinder_center_pipe_x @ translate_cylinder_center_pipe
    cylinder_center_pipe = Cylinder(30, crank_radius, 0.1)

    translate_cylinder_upper_axis = Mat4.from_translation(vector=Vec3(x=0, y=crank_radius/2, z=0))
    rotation_cylinder_upper_axis_x = Mat4.from_rotation(angle=math.pi/2, vector=Vec3(x=1, y=0, z=0))
    matrix_cylinder_upper_axis = matrix_cylinder_center_pipe @ translate_cylinder_upper_axis @ rotation_cylinder_upper_axis_x
    cylinder_upper_axis = Cylinder(30, 0.2, 0.2)

    translate_cylinder_upper_pipe = Mat4.from_translation(vector=Vec3(x=0, y=rod_length/2, z=0))
    rotation_cylinder_upper_pipe_x = Mat4.from_rotation(angle=-math.pi/2, vector=Vec3(x=1, y=0, z=0))
    matrix_cylinder_upper_pipe = matrix_cylinder_upper_axis @ rotation_cylinder_upper_pipe_x @ translate_cylinder_upper_pipe
    cylinder_upper_pipe = Cylinder(30, rod_length, 0.1)

    translate_cylinder_head_axis = Mat4.from_translation(vector=Vec3(x=0, y=rod_length/2, z=0))
    rotation_cylinder_head_axis_x = Mat4.from_rotation(angle=math.pi/2, vector=Vec3(x=1, y=0, z=0))
    matrix_cylinder_head_axis = matrix_cylinder_upper_pipe @ translate_cylinder_head_axis @ rotation_cylinder_head_axis_x
    cylinder_head_axis = Cylinder(30, 0.2, 0.2)

    translate_cylinder_head = Mat4.from_translation(vector=Vec3(x=0, y=0.25, z=0))
    rotation_cylinder_head = Mat4.from_rotation(angle=-math.pi/2, vector=Vec3(x=1, y=0, z=0))
    matrix_cylinder_head = matrix_cylinder_head_axis @ rotation_cylinder_head @ translate_cylinder_head
    cylinder_head = Cylinder(30, 0.5, 0.5)

    renderer.add_shape(matrix_cylinder_center_axis, cylinder_center_axis.vertices, cylinder_center_axis.indices, cylinder_center_axis.colors)
    renderer.add_shape(matrix_cylinder_center_pipe, cylinder_center_pipe.vertices, cylinder_center_pipe.indices, cylinder_center_pipe.colors)
    renderer.add_shape(matrix_cylinder_upper_axis, cylinder_upper_axis.vertices, cylinder_upper_axis.indices, cylinder_upper_axis.colors)
    renderer.add_shape(matrix_cylinder_upper_pipe, cylinder_upper_pipe.vertices, cylinder_upper_pipe.indices, cylinder_upper_pipe.colors)
    renderer.add_shape(matrix_cylinder_head_axis, cylinder_head_axis.vertices, cylinder_head_axis.indices, cylinder_head_axis.colors)
    renderer.add_shape(matrix_cylinder_head, cylinder_head.vertices, cylinder_head.indices, cylinder_head.colors)

def add_cog(x, y, z, height, radius, teeth):

    translate_cog_center = Mat4.from_translation(vector=Vec3(x=x, y=y, z=z))
    rotation_cog_center_x = Mat4.from_rotation(angle=math.pi/2, vector=Vec3(x=1, y=0, z=0))
    matrix_cog_center = translate_cog_center @ rotation_cog_center_x
    cylinder_cog_center = Cylinder(30, height, radius)
    renderer.add_shape(matrix_cog_center, cylinder_cog_center.vertices, cylinder_cog_center.indices, cylinder_cog_center.colors)

    # added teeth using cube
    for i in range(teeth):
        translate_cog_teeth = Mat4.from_translation(vector=Vec3(x=0, y=0, z=radius+height/2))
        rotation_cog_teeth = Mat4.from_rotation(angle=2*math.pi/teeth*i, vector=Vec3(x=0, y=1, z=0))
        matrix_cog_teeth = matrix_cog_center @ rotation_cog_teeth @ translate_cog_teeth
        cube_cog_teeth = Cube((height, height, height))
        renderer.add_shape(matrix_cog_teeth, cube_cog_teeth.vertices, cube_cog_teeth.indices, cube_cog_teeth.colors)

if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "Hello Pyglet", resizable = True)   
    renderer.set_location(200, 200)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)

    add_piston(0, 0, 0, math.pi/4)
    add_piston(0, 0, -0.5, 3*math.pi/4)
    add_piston(0, 0, -1, 5*math.pi/4)
    add_piston(0, 0, -1.5, 7*math.pi/4)
    add_piston(0, 0, -2, math.pi/4)
    add_piston(0, 0, -2.5, 3*math.pi/4)
    add_piston(0, 0, -3, 5*math.pi/4)
    add_piston(0, 0, -3.5, 7*math.pi/4)
    add_piston(0, 0, -4, math.pi/4)
    add_piston(0, 0, -4.5, 3*math.pi/4)
    add_piston(0, 0, -5, 5*math.pi/4)
    add_piston(0, 0, -5.5, 7*math.pi/4)
    add_piston(0, 0, -6, math.pi/4)
    add_piston(0, 0, -6.5, 3*math.pi/4)
    add_piston(0, 0, -7, 5*math.pi/4)
    add_piston(0, 0, -7.5, 7*math.pi/4)

    translate_axis = Mat4.from_translation(vector=Vec3(x=0, y=0, z=-3))
    rotation_axis = Mat4.from_rotation(angle=math.pi/2, vector=Vec3(x=1, y=0, z=0))
    matrix_axis = translate_axis @ rotation_axis
    cylinder_axis = Cylinder(30, 10, 0.1)
    renderer.add_shape(matrix_axis, cylinder_axis.vertices, cylinder_axis.indices, cylinder_axis.colors)

    add_cog(0, 0, 2, 0.3, 2, 20)
    add_cog(-3.3, 0, 2, 0.3, 1, 10)

    #draw shapes
    renderer.run()
