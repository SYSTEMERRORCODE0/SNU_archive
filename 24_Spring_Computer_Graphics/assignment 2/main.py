from pyglet.math import Mat4, Vec3
from pyglet.gl import GL_TRIANGLES, GL_LINES, GL_POINTS

from render import RenderWindow
from primitives import *
from control import Control

vertices, lines, triangles, surfaces = None, None, None, None

def load_object(filename):
    f = open(filename, 'r')

    total_vertices = []
    total_lines = []
    total_triangles = []
    total_surfaces = []
    total_start_vertex = []

    vertices = []
    triangles = []
    lines = []
    surfaces = []
    start_vertex = 0

    state = True

    while True:
        line = f.readline()

        if not line:
            break

        if line.startswith('v '):  # Vertex line
            if state == False:
                lines = list(set(lines))
                lines = [[x, y] for x, y in lines]
                total_vertices.append(vertices)
                total_lines.append(lines)
                total_triangles.append(triangles)
                total_surfaces.append(surfaces)
                total_start_vertex.append(start_vertex)
                start_vertex += len(vertices)
                vertices = []
                triangles = []
                lines = []
                surfaces = []
                state = True

            _, x, y, z = line.split()
            vertices.append(Vec3(x=float(x), y=float(y), z=float(z)))
        elif line.startswith('f '):  # Face line
            state = False
            parts = line.split()[1:]  # Ignore 'f' and split by spaces
            parts = [int(i)-1-start_vertex for i in parts]
            surfaces.append(parts)
            for i in range(2,len(parts)):
                triangles.append([parts[0], parts[i-1], parts[i]])
            for i in range(1, len(parts)):
                x = min(parts[i-1], parts[i])
                y = max(parts[i-1], parts[i])
                lines.append((x, y))
            x = min(parts[0], parts[-1])
            y = max(parts[0], parts[-1])
            lines.append((x, y))

    f.close()

    lines = list(set(lines))
    lines = [[x, y] for x, y in lines]
    total_vertices.append(vertices)
    total_lines.append(lines)
    total_triangles.append(triangles)
    total_surfaces.append(surfaces)
    total_start_vertex.append(start_vertex)

    return total_vertices, total_lines, total_triangles, total_surfaces, total_start_vertex

def add_pointSet(positions):
    '''
    Add a point set to the scene
    '''
    pointSet = PointSet(positions)
    pointSet_position = Mat4.from_translation(vector=Vec3(0,0,0))
    renderer.add_shape(pointSet_position, pointSet.vertices, pointSet.indices, pointSet.colors, PointGroup, mode=GL_POINTS)

def add_lineSet(positions, pairs):
    '''
    Add a line set to the scene
    '''
    lineSet = LineSet(positions, pairs)
    lineSet_position = Mat4.from_translation(vector=Vec3(0,0,0))
    renderer.add_shape(lineSet_position, lineSet.vertices, lineSet.indices, lineSet.colors, LineGroup, mode=GL_LINES)

def add_triangleSet(positions, triangles):
    '''
    Add a triangle set to the scene
    '''
    triangleSet = TriangleSet(positions, triangles)
    triangleSet_position = Mat4.from_translation(vector=Vec3(0,0,0))
    renderer.add_shape(triangleSet_position, triangleSet.vertices, triangleSet.indices, triangleSet.colors, TriangleGroup, mode=GL_TRIANGLES)

def add_derivedSurface():
    '''
    Add a derived surface object to the scene
    '''
    derivedSurface = DerivedSurface()
    derivedSurface_position = Mat4.from_translation(vector=Vec3(0,0,0))
    renderer.add_shape(derivedSurface_position, derivedSurface.vertices, derivedSurface.indices, derivedSurface.colors, DerivedSurfaceGroup, mode=GL_TRIANGLES)

def add_derivedLine():
    '''
    Add a derived line object to the scene
    '''
    derivedLine = DerivedLine()
    derivedLine_position = Mat4.from_translation(vector=Vec3(0,0,0))
    renderer.add_shape(derivedLine_position, derivedLine.vertices, derivedLine.indices, derivedLine.colors, DerivedLineGroup, mode=GL_LINES)

def add_derivedSubdivisionLine(v, e, f):
    '''
    Add a derived subdivision object to the scene
    '''
    derivedSubdivision = DerivedSubdivisionLine(v, e, f)
    derivedSubdivision_position = Mat4.from_translation(vector=Vec3(0,0,0))
    renderer.add_shape(derivedSubdivision_position, derivedSubdivision.vertices, derivedSubdivision.indices, derivedSubdivision.colors, DerivedSubdivisionLineGroup, mode=GL_LINES)

def add_derivedSubdivisionSurface(v, e, f):
    '''
    Add a derived subdivision object to the scene
    '''
    derivedSubdivision = DerivedSubdivisionSurface(v, e, f)
    derivedSubdivision_position = Mat4.from_translation(vector=Vec3(0,0,0))
    renderer.add_shape(derivedSubdivision_position, derivedSubdivision.vertices, derivedSubdivision.indices, derivedSubdivision.colors, DerivedSubdivisionSurfaceGroup, mode=GL_TRIANGLES)

if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "Hello Pyglet", resizable = True)   
    renderer.set_location(200, 200)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)

    # Load object
    #vertices, lines, triangles, surfaces = load_object('SurfaceMesh\Spline\grid.obj')
    #vertices, lines, triangles, surfaces = load_object('SurfaceMesh\Subdivision\cross_cube.obj')
    #vertices, lines, triangles, surfaces = load_object('SurfaceMesh\Subdivision\icosahedron.obj')
    
    filename = input("Input file name to load object (default : 'SurfaceMesh\Spline\grid_test.obj') >>> ")
    if filename == "":
        filename = 'SurfaceMesh\Spline\grid_test.obj'
    else:
        renderer.filename = filename

    vertices, lines, triangles, surfaces, start_vertex = load_object(filename)
    renderer.vertices = vertices
    renderer.lines = lines
    renderer.triangles = triangles
    renderer.surfaces = surfaces
    renderer.start_vertex = start_vertex

    # idx % 7 == 0 : point
    # idx % 7 == 1 : line
    # idx % 7 == 2 : triangle
    # idx % 7 == 3 : derived line
    # idx % 7 == 4 : derived surface
    # idx % 7 == 5 : derived subdivision line
    # idx % 7 == 6 : derived subdivision surface
    for i in range(len(vertices)):
        add_pointSet(vertices[i])
        add_lineSet(vertices[i], lines[i])
        add_triangleSet(vertices[i], triangles[i])
        add_derivedLine()
        add_derivedSurface()
        add_derivedSubdivisionLine(vertices[i], lines[i], surfaces[i])
        add_derivedSubdivisionSurface(vertices[i], lines[i], surfaces[i])

    #draw shapes
    renderer.run()
