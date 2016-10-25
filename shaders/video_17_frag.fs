#version 330
in vec2 newTexture;

out vec4 outColor;
uniform sampler2D samplerTexture;
void main()
{
    outColor = texture(samplerTexture, newTexture);
}