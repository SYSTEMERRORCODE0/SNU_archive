from pyglet.graphics.shader import Shader, ShaderProgram

# create vertex and fragment shader sources
vertex_source_default = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;

out vec4 newColor;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp
    newColor = colors;
}
"""

fragment_source_default = """
#version 330
in vec4 newColor;

out vec4 outColor;

void main()
{
    outColor = newColor;
}
"""

#
# Phong shading w/o textures
#
vertex_source_phong = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;
layout(location =2) in vec3 normals;

out vec4 newColor;
out vec3 Normal;
out vec3 FragPos;

uniform mat4 view_proj;
uniform mat4 model;
uniform vec3 lightPos; // Light position

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp
    newColor = colors;
    FragPos = vec3(model * vec4(vertices, 1.0f));
    Normal = mat3(transpose(inverse(model))) * normals;
}
"""

fragment_source_phong = """
#version 330
in vec4 newColor;
in vec3 Normal;
in vec3 FragPos;

out vec4 outColor;

uniform vec3 lightPos; // Light position
uniform vec3 viewPos; // View position
uniform vec3 lightColor; // Light color
uniform float lightIntensity; // Light intensity

void main()
{

    // Ambient
    float ambientStrength = 0.1f;
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse
    float diffuseStrength = 0.5f;
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float distSqr = length(lightPos - FragPos) * length(lightPos - FragPos);
    float diff = diffuseStrength * max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor * lightIntensity / distSqr;

    // Specular
    int shininess = 8;
    float specularStrength = 0.8f;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = specularStrength * spec * lightColor * lightIntensity / distSqr;

    vec3 result = (ambient + diffuse + specular);
    outColor = newColor * vec4(result, 1.0f);

}
"""

#
# Phong shading with textures
#
vertex_source_phong_texture = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec2 textures_vertices;
layout(location =2) in vec3 normals;

out vec3 Normal;
out vec3 FragPos;
out vec2 TextCoord;

uniform sampler2D textureBaseColor;
uniform mat4 view_proj;
uniform mat4 model;
uniform vec3 lightPos; // Light position

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp
    FragPos = vec3(model * vec4(vertices, 1.0f));
    Normal = mat3(transpose(inverse(model))) * normals;
    TextCoord = textures_vertices;
}
"""

fragment_source_phong_texture = """
#version 330
in vec3 Normal;
in vec3 FragPos;
in vec2 TextCoord;

out vec4 outColor;

uniform vec3 lightPos; // Light position
uniform vec3 viewPos; // View position
uniform vec3 lightColor; // Light color
uniform float lightIntensity; // Light intensity
uniform sampler2D textureBaseColor;
uniform sampler2D textureMixedAO;
uniform sampler2D textureRoughness;
uniform sampler2D textureSpecular;

void main()
{

    // Ambient
    float ambientStrength = texture(textureMixedAO, TextCoord).r / 255;
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse
    vec3 diffuseStrength = texture(textureBaseColor, TextCoord).rgb;
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float distSqr = length(lightPos - FragPos) * length(lightPos - FragPos);
    vec3 diff = diffuseStrength * max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor * lightIntensity / distSqr;

    // Specular
    float a = 0.1;
    float b = 0.1;
    float shininess = 1 / (a * texture(textureRoughness, TextCoord).r + b);
    vec3 specularStrength = texture(textureSpecular, TextCoord).rgb;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = specularStrength * spec * lightColor * lightIntensity / distSqr;

    vec3 result = (ambient + diffuse + specular);
    outColor = vec4(result, 1.0f);

}
"""

#
# Phong shading with textures and normal mapping
#
vertex_source_phong_texture_normal = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec2 textures_vertices;
layout(location =2) in vec3 normals;
layout(location =3) in vec3 deltaPos1;
layout(location =4) in vec3 deltaPos2;
layout(location =5) in vec2 deltaUV1;
layout(location =6) in vec2 deltaUV2;

out vec3 FragPos;
out vec2 TextCoord;
out mat3 TBN;

uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp
    FragPos = vec3(model * vec4(vertices, 1.0f));
    vec3 normal = normalize(mat3(transpose(inverse(model))) * normals);
    TextCoord = textures_vertices;

    // Calculate TBN matrix
    vec3 tangent = (deltaPos1 * deltaUV2.y - deltaPos2 * deltaUV1.y);
    vec3 bitangent = (deltaPos2 * deltaUV1.x - deltaPos1 * deltaUV2.x);
    tangent = normalize(tangent);
    bitangent = normalize(bitangent);
    TBN = mat3(tangent, bitangent, normal);

}
"""

fragment_source_phong_texture_normal = """
#version 330
in vec3 FragPos;
in vec2 TextCoord;
in mat3 TBN;

out vec4 outColor;

uniform mat4 model;
uniform vec3 lightPos; // Light position
uniform vec3 viewPos; // View position
uniform vec3 lightColor; // Light color
uniform float lightIntensity; // Light intensity
uniform sampler2D textureBaseColor;
uniform sampler2D textureMixedAO;
uniform sampler2D textureRoughness;
uniform sampler2D textureSpecular;
uniform sampler2D textureNormal;

void main()
{

    // Calculate normal from normal map
    vec3 normal_map = texture(textureNormal, TextCoord).rgb;
    normal_map = normal_map * 2.0 - 1.0;
    vec3 norm = normalize(TBN * normal_map);

    // Ambient
    float ambientStrength = texture(textureMixedAO, TextCoord).r / 255;
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse
    vec3 diffuseStrength = texture(textureBaseColor, TextCoord).rgb;
    vec3 lightDir = normalize(lightPos - FragPos);
    float distSqr = length(lightPos - FragPos) * length(lightPos - FragPos);
    vec3 diff = diffuseStrength * max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor * lightIntensity / distSqr;

    // Specular
    float a = 0.1;
    float b = 0.1;
    float shininess = 1 / (a * texture(textureRoughness, TextCoord).r + b);
    vec3 specularStrength = texture(textureSpecular, TextCoord).rgb;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = specularStrength * spec * lightColor * lightIntensity / distSqr;

    vec3 result = (ambient + diffuse + specular);
    outColor = vec4(result, 1.0f);

}
"""


def create_program(vs_source, fs_source):
    # compile the vertex and fragment sources to a shader program
    vert_shader = Shader(vs_source, 'vertex')
    frag_shader = Shader(fs_source, 'fragment')
    return ShaderProgram(vert_shader, frag_shader)