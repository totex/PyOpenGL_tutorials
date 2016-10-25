#version 330
in layout(location = 0) vec3 position;
in layout(location = 1) vec2 textureCoords;

uniform mat4 transform;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

out vec2 newTexture;
void main()
{
    gl_Position = projection * view * model * transform * vec4(position, 1.0f);
    newTexture = textureCoords;
}