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

        self.selected_point = None
        self.mouse_move_camera = False
        self.dragging = False

        self.surface_mode = self.NO_SURFACE
        self.vertex_attach = False
        self.vertex_integer = False
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
        elif symbol == pyglet.window.key.F:
            self.surface_mode_control(self.BEZIER_SURFACE)
        elif symbol == pyglet.window.key.G:
            self.surface_mode_control(self.BSPLINE_SURFACE)
        elif symbol == pyglet.window.key.R:
            self.surface_mode_control(self.SUBDIVISION_SURFACE)
        elif symbol == pyglet.window.key.Q:
            self.vertex_attach = True
        elif symbol == pyglet.window.key.E:
            self.vertex_integer = True
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
        elif symbol == pyglet.window.key.Q:
            self.vertex_attach = False
        elif symbol == pyglet.window.key.E:
            self.vertex_integer = False
        # TODO:
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        # TODO:
        pass

    def on_mouse_press(self, x, y, button, modifier):
        '''
        when mouse left is pressed, select a point on the screen,
        when mouse right is pressed, rotate the camera
        '''
        if button == mouse.LEFT:
            self.selected_point = self.find_point(x, y)
            print(self.selected_point)
        elif button == mouse.RIGHT:
            self.mouse_move_camera = True
        

    def on_mouse_release(self, x, y, button, modifier):
        if button == mouse.LEFT:
            if self.selected_point != None and self.vertex_attach == True:
                self.near_point()
            if self.selected_point != None and self.vertex_integer == True:
                self.integer_point()
            self.selected_point = None
            self.dragging = False
        elif button == mouse.RIGHT:
            self.window.camera_mouse_move_x = 0
            self.window.camera_mouse_move_y = 0
            self.mouse_move_camera = False

    def on_mouse_drag(self, x, y, dx, dy, button, modifier):
        if self.selected_point is not None and button == mouse.LEFT:
            self.move_vertex(dx, dy)

        elif button == mouse.RIGHT:
            self.window.camera_mouse_move_x = dx / 3
            self.window.camera_mouse_move_y = dy / 3

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # TODO:
        pass


    '''
    assistant functions for control
    '''
    def move_vertex(self, dx, dy):
        self.dragging = True
        idx, shape, i, point = self.selected_point

        normal_vec = (self.window.cam_target - self.window.cam_eye).normalize()
        right_vec = normal_vec.cross(self.window.cam_vup).normalize()
        up_vec = right_vec.cross(normal_vec).normalize()

        point_depth = (point - self.window.cam_eye).mag

        mouse_move_vec_x = right_vec * dx
        mouse_move_vec_y = up_vec * dy

        mouse_move_vec = (mouse_move_vec_x + mouse_move_vec_y) * point_depth / (self.window.width / 2)

        point.x += mouse_move_vec.x
        point.y += mouse_move_vec.y
        point.z += mouse_move_vec.z

        self.update_vertex(idx, i, point)

    def update_vertex(self, idx, i, point):

        vertexset = self.window.shapes[idx]

        vertexset.indexed_vertices_list.vertices[i*3] = point.x
        vertexset.indexed_vertices_list.vertices[i*3+1] = point.y
        vertexset.indexed_vertices_list.vertices[i*3+2] = point.z

        lineset = self.window.shapes[idx+1]
        triangleset = self.window.shapes[idx+2]

        lineset.indexed_vertices_list.vertices[i*3] = point.x
        lineset.indexed_vertices_list.vertices[i*3+1] = point.y
        lineset.indexed_vertices_list.vertices[i*3+2] = point.z

        triangleset.indexed_vertices_list.vertices[i*3] = point.x
        triangleset.indexed_vertices_list.vertices[i*3+1] = point.y
        triangleset.indexed_vertices_list.vertices[i*3+2] = point.z

        self.window.vertices[idx // 7][i].x = point.x
        self.window.vertices[idx // 7][i].y = point.y
        self.window.vertices[idx // 7][i].z = point.z

        if self.surface_mode == self.BEZIER_SURFACE or self.surface_mode == self.BEZIER_INVISIBLE:
            self.add_bezier_surface(idx)
        elif self.surface_mode == self.BSPLINE_SURFACE or self.surface_mode == self.BSPLINE_INVISIBLE:
            self.add_bspline_surface(idx)
        elif self.surface_mode == self.SUBDIVISION_SURFACE or self.surface_mode == self.SUBDIVISION_INVISIBLE:
            self.subdivision_surface(idx)


    def is_clicked(self, x, y, point):
        px, py = self.point_projection(point)
        select_range = 10

        if x - select_range <= px <= x + select_range and y - select_range <= py <= y + select_range:
            return True
        return False


    def find_point(self, x, y):
        '''
        Find the point that is clicked on the screen
        '''
        for idx, shape in enumerate(self.window.shapes):
            if shape.__class__.__name__ == 'PointGroup':
                point_num = len(shape.indexed_vertices_list.vertices) // 3
                points = shape.indexed_vertices_list.vertices
                for i in range(point_num):
                    px = points[i*3]
                    py = points[i*3+1]
                    pz = points[i*3+2]
                    point = Vec3(px, py, pz)
                    if self.is_clicked(x, y, point):
                        return idx, shape, i, point
        
        return None
                    
    def near_point(self):
        '''
        Check if the selected point is near to any other points when released
        '''

        sel_idx, sel_shape, sel_i, sel_point = self.selected_point
        screened_sel_point = self.point_projection(sel_point)

        for idx, shape in enumerate(self.window.shapes):
            if shape.__class__.__name__ == 'PointGroup':
                point_num = len(shape.indexed_vertices_list.vertices) // 3
                points = shape.indexed_vertices_list.vertices
                for i in range(point_num):
                    if sel_idx == idx and sel_i == i:
                        continue
                    px = points[i*3]
                    py = points[i*3+1]
                    pz = points[i*3+2]
                    point = Vec3(px, py, pz)

                    screened_point = self.point_projection(point)
                    if (screened_point[0] - screened_sel_point[0])**2 + (screened_point[1] - screened_sel_point[1])**2 < 100:
                        sel_point.x = point.x
                        sel_point.y = point.y
                        sel_point.z = point.z
                        self.update_vertex(sel_idx, sel_i, sel_point)
                        return idx, shape, i, point
                    
        return None
    
    def integer_point(self):
        '''
        Change the selected point to integer
        '''
        sel_idx, sel_shape, sel_i, sel_point = self.selected_point

        sel_point.x = round(sel_point.x)
        sel_point.y = round(sel_point.y)
        sel_point.z = round(sel_point.z)

        self.update_vertex(sel_idx, sel_i, sel_point)
                    
    def point_projection(self, point):
        point_proj = self.window.proj_mat @ self.window.view_mat @ Vec4(point.x, point.y, point.z, 1)
        point_proj = point_proj / point_proj.w

        x = (point_proj.x + 1) * self.window.width / 2
        y = (point_proj.y + 1) * self.window.height / 2
        return x, y
    


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
        if self.surface_mode == mode:
            self.surface_mode = - mode
            for idx, shape in enumerate(self.window.shapes):
                if (shape.__class__.__name__ == 'DerivedLineGroup' or 
                    shape.__class__.__name__ == 'DerivedSurfaceGroup' or 
                    shape.__class__.__name__ == 'DerivedSubdivisionLineGroup' or 
                    shape.__class__.__name__ == 'DerivedSubdivisionSurfaceGroup'):
                    self.window.shapes[idx].visible = 0
                elif shape.__class__.__name__ == 'TriangleGroup':
                    self.window.shapes[idx].visible = 1
                    

        elif self.surface_mode == - mode:
            self.surface_mode = mode
            for idx, shape in enumerate(self.window.shapes):
                if (mode == self.BEZIER_SURFACE or mode == self.BSPLINE_SURFACE):
                    if ((shape.__class__.__name__ == 'DerivedLineGroup' or 
                        shape.__class__.__name__ == 'DerivedSurfaceGroup')):
                        self.window.shapes[idx].visible = 1
                    elif ((shape.__class__.__name__ == 'DerivedSubdivisionLineGroup' or 
                        shape.__class__.__name__ == 'DerivedSubdivisionSurfaceGroup')):
                        self.window.shapes[idx].visible = 0
                    elif shape.__class__.__name__ == 'TriangleGroup':
                        self.window.shapes[idx].visible = 0
                elif mode == self.SUBDIVISION_SURFACE:
                    if ((shape.__class__.__name__ == 'DerivedLineGroup' or 
                        shape.__class__.__name__ == 'DerivedSurfaceGroup')):
                        self.window.shapes[idx].visible = 0
                    elif ((shape.__class__.__name__ == 'DerivedSubdivisionLineGroup' or 
                        shape.__class__.__name__ == 'DerivedSubdivisionSurfaceGroup')):
                        self.window.shapes[idx].visible = 1
                    elif shape.__class__.__name__ == 'TriangleGroup':
                        self.window.shapes[idx].visible = 0

        elif mode != self.NO_CHANGE:
            self.surface_mode = mode
            if mode == self.BEZIER_SURFACE:
                for idx, shape in enumerate(self.window.shapes):
                    if shape.__class__.__name__ == 'DerivedLineGroup' or shape.__class__.__name__ == 'DerivedSurfaceGroup':
                        self.window.shapes[idx].visible = 1
                    elif shape.__class__.__name__ == 'DerivedSubdivisionLineGroup' or shape.__class__.__name__ == 'DerivedSubdivisionSurfaceGroup':
                        self.window.shapes[idx].visible = 0
                    elif shape.__class__.__name__ == 'TriangleGroup':
                        self.window.shapes[idx].visible = 0
                    if shape.__class__.__name__ == 'PointGroup' and len(shape.indexed_vertices_list.vertices) == 48:
                        self.add_bezier_surface(idx, shape)
            elif mode == self.BSPLINE_SURFACE:
                for idx, shape in enumerate(self.window.shapes):
                    if shape.__class__.__name__ == 'DerivedLineGroup' or shape.__class__.__name__ == 'DerivedSurfaceGroup':
                        self.window.shapes[idx].visible = 1
                    elif shape.__class__.__name__ == 'DerivedSubdivisionLineGroup' or shape.__class__.__name__ == 'DerivedSubdivisionSurfaceGroup':
                        self.window.shapes[idx].visible = 0
                    elif shape.__class__.__name__ == 'TriangleGroup':
                        self.window.shapes[idx].visible = 0
                    if shape.__class__.__name__ == 'PointGroup' and len(shape.indexed_vertices_list.vertices) == 48:
                        self.add_bspline_surface(idx, shape)
            elif mode == self.SUBDIVISION_SURFACE:
                for idx, shape in enumerate(self.window.shapes):
                    if shape.__class__.__name__ == 'DerivedLineGroup' or shape.__class__.__name__ == 'DerivedSurfaceGroup':
                        self.window.shapes[idx].visible = 0
                    elif shape.__class__.__name__ == 'DerivedSubdivisionLineGroup' or shape.__class__.__name__ == 'DerivedSubdivisionSurfaceGroup':
                        self.window.shapes[idx].visible = 1
                    elif shape.__class__.__name__ == 'TriangleGroup':
                        self.window.shapes[idx].visible = 0
                    if shape.__class__.__name__ == 'PointGroup':
                        self.subdivision_surface(idx, shape)

        if self.grid_visible == False:
            for idx, shape in enumerate(self.window.shapes):
                if shape.__class__.__name__ == 'PointGroup' or shape.__class__.__name__ == 'LineGroup':
                    self.window.shapes[idx].visible = 0
        else :
            for idx, shape in enumerate(self.window.shapes):
                if shape.__class__.__name__ == 'PointGroup' or shape.__class__.__name__ == 'LineGroup':
                    self.window.shapes[idx].visible = 1


        print("surface Mode : ", self.surface_mode)
        
            


    '''
    Add Bezier surface or B-Spline surface
    Only works when the 16 points exists in pointset
    '''

    def bernstein_poly(self, i, n, u):
        return math.comb(n, i) * (u**i) * ((1-u)**(n-i))

    def add_bezier_surface(self, idx, shape = None):
        
        raw_grid_vertices = self.window.shapes[idx].indexed_vertices_list.vertices
        grid_vertices = []
        for i in range(len(raw_grid_vertices) // 3):
            grid_vertices.append(Vec3(x=raw_grid_vertices[i*3], y=raw_grid_vertices[i*3+1], z=raw_grid_vertices[i*3+2]))
        
        surface_vertices = []

        # bezier surface points 10 * 10
        n = 10

        for i in range(0, 10):
            for j in range(0, 10):
                
                u = i / 9
                v = j / 9

                surface_vertex = Vec3(0, 0, 0)

                for k in range(4):
                    for l in range(4):
                        surface_vertex += grid_vertices[k*4+l] * self.bernstein_poly(k, 3, u) * self.bernstein_poly(l, 3, v)
                
                surface_vertices.append(surface_vertex.x)
                surface_vertices.append(surface_vertex.y)
                surface_vertices.append(surface_vertex.z)

        self.window.shapes[idx+3].indexed_vertices_list.vertices = surface_vertices
        self.window.shapes[idx+4].indexed_vertices_list.vertices = surface_vertices
                

    def bspline_matrix(self, i, u):
        if i == 0:
            return (1/6) * ((1-u)**3)
        elif i == 1:
            return (1/6) * (3*u**3 - 6*u**2 + 4)
        elif i == 2:
            return (1/6) * (-3*u**3 + 3*u**2 + 3*u + 1)
        elif i == 3:
            return (1/6) * (u**3)

    def add_bspline_surface(self, idx, shape = None):
        raw_grid_vertices = self.window.shapes[idx].indexed_vertices_list.vertices
        grid_vertices = []
        for i in range(len(raw_grid_vertices) // 3):
            grid_vertices.append(Vec3(x=raw_grid_vertices[i*3], y=raw_grid_vertices[i*3+1], z=raw_grid_vertices[i*3+2]))
        
        surface_vertices = []

        # bspline surface points 10 * 10
        n = 10

        for i in range(0, 10):
            for j in range(0, 10):
                
                u = i / 9
                v = j / 9

                surface_vertex = Vec3(0, 0, 0)

                for k in range(4):
                    for l in range(4):
                        surface_vertex += grid_vertices[k*4+l] * self.bspline_matrix(k, u) * self.bspline_matrix(l, v)
                
                surface_vertices.append(surface_vertex.x)
                surface_vertices.append(surface_vertex.y)
                surface_vertices.append(surface_vertex.z)

        self.window.shapes[idx+3].indexed_vertices_list.vertices = surface_vertices
        self.window.shapes[idx+4].indexed_vertices_list.vertices = surface_vertices

    def subdivision_surface(self, idx, shape = None):
        
        face_midpoints = []
        edge_midpoints = []
        modified_vertices = []
        vertices = []
        lines = []
        surfaces = []
        triangles = []
        edge_to_face = {}
        vertex_to_edge = {}

        raw_vertices = self.window.vertices[idx // 7]
        raw_lines = self.window.lines[idx // 7]
        raw_surfaces = self.window.surfaces[idx // 7]

        surface_num = len(raw_surfaces)
        line_num = len(raw_lines)

        # add a point of average of surface vertices
        for surface in raw_surfaces:
            surface_point = Vec3(0, 0, 0)
            for vertex in surface:
                surface_point += raw_vertices[vertex]
            surface_point = surface_point / len(surface)
            
            face_midpoints.append(surface_point)
            vertices.append(surface_point)

        # add a point of average of 2 line vertices and 2 contact surface vertices
        for i, line in enumerate(raw_lines):
            line_point = Vec3(0, 0, 0)
            x = line[0]
            y = line[1]
            line_point += raw_vertices[x] + raw_vertices[y]

            boundary = 2
            addition = Vec3(0, 0, 0)

            connected_face = []
            for j, surface in enumerate(raw_surfaces):
                if x in surface and y in surface:
                    addition += face_midpoints[j]
                    boundary -= 1
                    connected_face.append(j)
                    lines.append([j, i+surface_num])

            edge_to_face[i] = connected_face
            

            if boundary > 0:
                line_point = line_point / 2
            else:
                line_point = (line_point + addition) / 4
            
            edge_midpoints.append(line_point)
            vertices.append(line_point)

        # add a modified point of original vertices
        for i, vertex in enumerate(raw_vertices):

            # Average of edge midpoints

            n = 0
            R = Vec3(0, 0, 0)
            connected_lines = []
            for j, line in enumerate(raw_lines):
                if i in line:
                    R += (raw_vertices[line[0]] + raw_vertices[line[1]]) / 2
                    n += 1
                    connected_lines.append(j)
                    lines.append([j+surface_num, i+surface_num+line_num])
            R = R / n
            vertex_to_edge[i] = connected_lines

            # Average of face points

            m = 0
            F = Vec3(0, 0, 0)
            connected_face = []
            for j, surface in enumerate(raw_surfaces):
                if i in surface:
                    ind = surface.index(i)
                    x = surface[ind-1]
                    y = surface[(ind+1)%len(surface)]

                    prev = 0
                    next = 0
                    for k, line in enumerate(raw_lines):
                        if x in line and i in line:
                            prev = k
                        if y in line and i in line:
                            next = k

                    m += 1

                    surfaces.append([j, prev+surface_num, i+surface_num+line_num, next+surface_num])
                    triangles.append([j, prev+surface_num, i+surface_num+line_num])
                    triangles.append([j, i+surface_num+line_num, next+surface_num])

                    F += face_midpoints[j]
                    connected_face.append(j)
            F = F / m

            vertex_point = (vertex * (n-3) + R * 2 + F) / n

            modified_vertices.append(vertex_point)
            vertices.append(vertex_point)

        update_vertices = []
        for vertex in vertices:
            update_vertices.append(vertex.x)
            update_vertices.append(vertex.y)
            update_vertices.append(vertex.z)

        #print([len(i.indexed_vertices_list.vertices) for i in self.window.shapes])
        #print([len(i.indexed_vertices_list.indices) for i in self.window.shapes])
        #print(len(update_vertices), len(vertices), len(lines), len(triangles))
        #print(lines)
        
        self.window.shapes[idx+5].indexed_vertices_list.vertices = update_vertices
        self.window.shapes[idx+5].indexed_vertices_list.indices = [i for j in lines for i in j]
        self.window.shapes[idx+6].indexed_vertices_list.vertices = update_vertices
        self.window.shapes[idx+6].indexed_vertices_list.indices = [i for j in triangles for i in j]


        