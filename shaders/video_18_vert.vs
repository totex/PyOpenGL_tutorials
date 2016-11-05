#version 330
in layout(location = 0) vec3 position;
in layout(location = 1) vec2 textureCoords;
in layout(location = 2) vec3 vertNormal;

uniform mat4 transform;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

uniform mat4 light;

out vec2 newTexture;
out vec3 fragNormal;

void main()
{
    fragNormal = (light * vec4(vertNormal, 0.0f)).xyz;
    gl_Position = projection * view * model * transform * vec4(position, 1.0f);
    newTexture = textureCoords;
}