import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key
from pyglet.math import Mat4, Vec3, Vec4
from primitives import *


class Control:

    '''
    surface mode
    '''
    NO_CHANGE = 9999
    NO_SURFACE = 0
    BEZIER_SURFACE = 1
    BEZIER_INVISIBLE = -1
    BSPLINE_SURFACE = 2
    BSPLINE_INVISIBLE = -2
    SUBDIVISION_SURFACE = 3
    SUBDIVISION_INVISIBLE = -3

    """
    Control class controls keyboard & mouse inputs.
    """
    def __init__(self, window):
        window.on_key_press = self.on_key_press
        window.on_key_release = self.on_key_release
        window.on_mouse_motion = self.on_mouse_motion
        window.on_mouse_drag = self.on_mouse_drag
        window.on_mouse_press = self.on_mouse_press
        window.on_mouse_release = self.on_mouse_release
        window.on_mouse_scroll = self.on_mouse_scroll
        self.window = window

        self.mouse_move_camera = False
        self.dragging = False

        self.grid_visible = True

        self.setup()

    def setup(self):
        pass

    def update(self, vector):
        pass

    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.W:
            self.window.camera_move_z += 1
        elif symbol == pyglet.window.key.S:
            self.window.camera_move_z -= 1
        elif symbol == pyglet.window.key.A:
            self.window.camera_move_x -= 1
        elif symbol == pyglet.window.key.D:
            self.window.camera_move_x += 1
        elif symbol == pyglet.window.key.LSHIFT:
            self.window.camera_move_y -= 1
        elif symbol == pyglet.window.key.SPACE:
            self.window.camera_move_y += 1
        elif symbol == pyglet.window.key.Z:
            self.grid_visible = not self.grid_visible
            self.surface_mode_control(self.NO_CHANGE)
        

        #self.window.setup()
    
    def on_key_release(self, symbol, modifier):
        if symbol == pyglet.window.key.ESCAPE:
            self.exit_work()
            pyglet.app.exit()
        elif symbol == pyglet.window.key.SPACE:
            self.window.camera_move_y -= 1
        elif symbol == pyglet.window.key.LSHIFT:
            self.window.camera_move_y += 1
        elif symbol == pyglet.window.key.W:
            self.window.camera_move_z -= 1
        elif symbol == pyglet.window.key.S:
            self.window.camera_move_z += 1
        elif symbol == pyglet.window.key.A:
            self.window.camera_move_x += 1
        elif symbol == pyglet.window.key.D:
            self.window.camera_move_x -= 1
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifier):
        '''
        when mouse left is pressed, select a point on the screen,
        when mouse right is pressed, rotate the camera
        '''
        if button == mouse.LEFT:
            pass
        elif button == mouse.RIGHT:
            self.mouse_move_camera = True
        

    def on_mouse_release(self, x, y, button, modifier):
        if button == mouse.LEFT:
            pass
        elif button == mouse.RIGHT:
            self.window.camera_mouse_move_x = 0
            self.window.camera_mouse_move_y = 0
            self.mouse_move_camera = False

    def on_mouse_drag(self, x, y, dx, dy, button, modifier):
        if button == mouse.LEFT:
            pass

        elif button == mouse.RIGHT:
            self.window.camera_mouse_move_x = dx / 3
            self.window.camera_mouse_move_y = dy / 3

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # TODO:
        pass


    '''
    save and exit functions
    '''

    def save_object(self, filename, vertices, lines, triangles, surfaces, start_vertex):
        if start_vertex ==0:
            f = open(filename, 'w')
        else:
            f = open(filename, 'a')

        for vertex in vertices:
            f.write(f'v {vertex.x} {vertex.y} {vertex.z}\n')

        for surface in surfaces:
            f.write('f ')
            for vertex in surface:
                f.write(f'{vertex+1+start_vertex} ')
            f.write('\n')

        f.close()

    def exit_work(self):
        save = input("Do you want to save the object? (y/n) >>> ")
        if save == 'y':
            filename = input(f"Input file name to save object (default : {self.window.filename}) >>> ")
            if filename == "":
                filename = self.window.filename
            window = self.window

            num = 0

            for idx, shape in enumerate(window.shapes):
                if shape.__class__.__name__ == 'PointGroup':
                    vertices_raw = shape.indexed_vertices_list.vertices
                    self.save_object(filename, window.vertices[num], window.lines[num], window.triangles[num], window.surfaces[num], window.start_vertex[num])
                    num += 1
        else:
            print("Exit without saving the object.")

    '''
    surface controller
    '''
    def surface_mode_control(self, mode = NO_CHANGE):
        #example of this function
        if self.surface_mode == mode:
            for idx, shape in enumerate(self.window.shapes):
                if (shape.__class__.__name__ == 'DerivedLineGroup' or 
                    shape.__class__.__name__ == 'DerivedSurfaceGroup' or 
                    shape.__class__.__name__ == 'DerivedSubdivisionLineGroup' or 
                    shape.__class__.__name__ == 'DerivedSubdivisionSurfaceGroup'):
                    self.window.shapes[idx].visible = 0
                elif shape.__class__.__name__ == 'TriangleGroup':
                    self.window.shapes[idx].visible = 1
                    
        
            