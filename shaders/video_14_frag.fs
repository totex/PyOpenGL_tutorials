#version 330
in vec3 newColor;
in vec2 newTexture;

out vec4 outColor;
uniform sampler2D samplerTexture;
void main()
{
    outColor = texture(samplerTexture, newTexture); //* vec4(newColor, 1.0f);
}