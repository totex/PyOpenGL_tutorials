import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import pyrr
from PIL import Image


def main():

    # initialize glfw
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    #        positions         colors          texture coords
    cube = [-0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0]

    cube = numpy.array(cube, dtype = numpy.float32)

    indices = [ 0,  1,  2,  2,  3,  0,
                4,  5,  6,  6,  7,  4,
                8,  9, 10, 10, 11,  8,
               12, 13, 14, 14, 15, 12,
               16, 17, 18, 18, 19, 16,
               20, 21, 22, 22, 23, 20]

    indices = numpy.array(indices, dtype= numpy.uint32)

    vertex_shader = """
    #version 330
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec3 color;
    in layout(location = 2) vec2 textureCoords;
    uniform mat4 transform;
    out vec3 newColor;
    out vec2 newTexture;
    void main()
    {
        gl_Position = transform * vec4(position, 1.0f);
        newColor = color;
        newTexture = textureCoords;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;
    in vec2 newTexture;

    out vec4 outColor;
    uniform sampler2D samplerTexture;
    void main()
    {
        outColor = texture(samplerTexture, newTexture) * vec4(newColor, 1.0f);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #color
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    #texture
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, cube.itemsize * 8, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)


    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open("res/crate.jpg")
    img_data = numpy.array(list(image.getdata()), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glEnable(GL_TEXTURE_2D)


    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time() )
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time() )

        transformLoc = glGetUniformLocation(shader, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, rot_x * rot_y)

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()