from pyglet.math import Mat4, Vec3
from pyglet.gl import GL_TRIANGLES, GL_LINES, GL_POINTS

from render import RenderWindow
from primitives import *
from control import Control

vertices, lines, triangles, surfaces = None, None, None, None

def load_object(filename):
    f = open(filename, 'r')

    vertices = []
    vertices_texture = []
    vertices_normal = []
    triangles = []
    triangles_texture = []
    triangles_normal = []
    lines = []
    surfaces = []

    total_objects = []

    while True:
        line = f.readline()

        if not line:
            break

        if line.startswith('v '):  # Vertex line
            _, x, y, z = line.split()
            vertices.append(Vec3(x=float(x), y=float(y), z=float(z)))

        elif line.startswith('vt '):  # Vertex texture line
            _, x, y, z = line.split()
            vertices_texture.append(Vec3(x=float(x), y=float(y), z=float(z)))

        elif line.startswith('vn '):  # Vertex normal line
            _, x, y, z = line.split()
            vertices_normal.append(Vec3(x=float(x), y=float(y), z=float(z)))

        elif line.startswith('f '):  # Face line
            parts = line.split()[1:]  # Ignore 'f' and split by spaces
            parts = [i for i in parts]
            parts_line = [int(i.split('/')[0])-1 for i in parts]

            surfaces.append(parts)
            for i in range(2, len(parts)):
                triangles.append([int(parts[0].split('/')[0])-1, 
                                  int(parts[i-1].split('/')[0])-1, 
                                  int(parts[i].split('/')[0])-1])
                triangles_texture.append([int(parts[0].split('/')[1])-1, 
                                          int(parts[i-1].split('/')[1])-1, 
                                          int(parts[i].split('/')[1])-1])
                triangles_normal.append([int(parts[0].split('/')[2])-1, 
                                         int(parts[i-1].split('/')[2])-1, 
                                         int(parts[i].split('/')[2])-1])
            for i in range(1, len(parts)):
                x = min(parts_line[i-1], parts_line[i])
                y = max(parts_line[i-1], parts_line[i])
                lines.append((x, y))
            x = min(parts_line[0], parts_line[-1])
            y = max(parts_line[0], parts_line[-1])
            lines.append((x, y))

        elif line.startswith('s '):
            if len(surfaces) > 0:
                lines = list(set(lines))
                lines = [[x, y] for x, y in lines]
                total_objects.append({"lines":lines, 
                                      "triangles":triangles,
                                      "triangles_texture":triangles_texture,
                                      "triangles_normal":triangles_normal,
                                      "surfaces":surfaces})
                surfaces = []
                triangles = []
                lines = []

    f.close()

    lines = list(set(lines))
    lines = [[x, y] for x, y in lines]
    total_objects.append({"lines":lines, 
                            "triangles":triangles,
                            "triangles_texture":triangles_texture,
                            "triangles_normal":triangles_normal,
                            "surfaces":surfaces})

    return vertices, vertices_texture, vertices_normal, total_objects

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

def group_int_to_group(group_int):
    if group_int == 1:
        return TriangleGroup
    elif group_int == 2:
        return PhongTriangleGroup
    elif group_int == 3:
        return PhongWithTextureTriangleGroup
    elif group_int == 4:
        return PhongWithTextureWithNormalTriangleGroup
    else:
        return TriangleGroup

def add_triangleSet(positions, triangles, triangle_texture, triangle_normal, textures, normals, group = TriangleGroup,
                    textureBaseColorFilename = None, textureMixedAOFilename = None, textureNormalFilename = None, textureRoughnessFilename = None, textureSpecularFilename = None):
    '''
    Add a triangle set to the scene
    '''
    triangleSet = TriangleSet(positions, triangles, triangle_texture, triangle_normal, textures, normals)
    #print(len(triangleSet.vertices), len(triangleSet.normals), len(triangleSet.textures))
    triangleSet_position = Mat4.from_translation(vector=Vec3(0,0,0))
    renderer.add_shape(triangleSet_position, triangleSet.vertices, triangleSet.indices, triangleSet.colors, triangleSet.textures, triangleSet.normals, group, mode=GL_TRIANGLES, 
                       textureBaseColorFilename = textureBaseColorFilename,
                       textureMixedAOFilename = textureMixedAOFilename,
                       textureNormalFilename = textureNormalFilename,
                       textureRoughnessFilename = textureRoughnessFilename,
                       textureSpecularFilename = textureSpecularFilename,
                       deltaPos1 = triangleSet.deltaPos1, deltaPos2 = triangleSet.deltaPos2, deltaUV1 = triangleSet.deltaUV1, deltaUV2 = triangleSet.deltaUV2)


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

    filename = input("Input file name to load object (default : 'Free_rock.obj') >>> ")
    if filename == "":
        filename = 'Free_rock.obj'
    else:
        renderer.filename = filename

    textureBaseColorFilename = input("Input texture file name for base color (default : 'Free_rock_tex\Free_rock_Base_Color.jpg') >>> ")
    if textureBaseColorFilename == "":
        textureBaseColorFilename = 'Free_rock_tex\Free_rock_Base_Color.jpg'
    #renderer.textureBaseColorFilename = textureBaseColorFilename

    textureMixedAOFilename = input("Input texture file name for mixed AO (default : 'Free_rock_tex\Free_rock_Mixed_AO.jpg') >>> ")
    if textureMixedAOFilename == "":
        textureMixedAOFilename = 'Free_rock_tex\Free_rock_Mixed_AO.jpg'
    #renderer.textureMixedAOFilename = textureMixedAOFilename

    textureNormalFilename = input("Input texture file name for normal (default : 'Free_rock_tex\Free_rock_Normal_OpenGL.jpg') >>> ")
    if textureNormalFilename == "":
        textureNormalFilename = 'Free_rock_tex\Free_rock_Normal_OpenGL.jpg'
    #renderer.textureNormalFilename = textureNormalFilename

    textureRoughnessFilename = input("Input texture file name for roughness (default : 'Free_rock_tex\Free_rock_Roughness.jpg') >>> ")
    if textureRoughnessFilename == "":
        textureRoughnessFilename = 'Free_rock_tex\Free_rock_Roughness.jpg'
    #renderer.textureRoughnessFilename = textureRoughnessFilename

    textureSpecularFilename = input("Input texture file name for specular (default : 'Free_rock_tex\Free_rock_Specular.jpg') >>> ")
    if textureSpecularFilename == "":
        textureSpecularFilename = 'Free_rock_tex\Free_rock_Specular.jpg'
    #renderer.textureSpecularFilename = textureSpecularFilename

    rendering_group = input("Input rendering number (default : 'Wireframe')\n" \
                            " 1 : Wireframe\n" \
                            " 2 : Phong shading w/o textures\n" \
                            " 3 : Phong shading w/ textures\n" \
                            " 4 : Phong shading w/ textures w/ normal \n" \
                            ">>> ")
    if rendering_group == "":
        rendering_group = "1"

    rendering_group = group_int_to_group(int(rendering_group))

    vertices, vertices_texture, vertices_normal, total_objects = load_object(filename)
    renderer.vertices = vertices
    renderer.vertices_texture = vertices_texture
    renderer.vertices_normal = vertices_normal
    renderer.total_objects = total_objects


    #add_pointSet(vertices)
    for obj in total_objects:
        if rendering_group == TriangleGroup:
            add_lineSet(vertices, [i for i in obj['lines']])
        add_triangleSet(vertices, [i for i in obj['triangles']], [i for i in obj['triangles_texture']], [i for i in obj['triangles_normal']], vertices_texture, vertices_normal, rendering_group,
                        textureBaseColorFilename, textureMixedAOFilename, textureNormalFilename, textureRoughnessFilename, textureSpecularFilename)

    #draw shapes
    renderer.run()
