import glfw

from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_array_object import *

import numpy

vs_source = """
#version 150 core

in vec3 in_position;

void main(void) 
{
    gl_Position = vec4( in_position, 1.0 );
}
"""

fs_source = """
#version 150 core

out vec4 out_frag_color;

void main(void) 
{
    out_frag_color = vec4( 0.0, 1.0, 0.0, 1.0 );
}
"""

glfw.Init()

glfw.OpenWindowHint( glfw.OPENGL_VERSION_MAJOR, 3 )
glfw.OpenWindowHint( glfw.OPENGL_VERSION_MINOR, 2 )
glfw.OpenWindowHint( glfw.OPENGL_FORWARD_COMPAT, GL_TRUE )
glfw.OpenWindowHint( glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE )

glfw.OpenWindow(
    800, 600,
    8, 8, 8,
    8, 24, 0,
    glfw.WINDOW
    )

glfw.SetWindowTitle( "GLFW" )

print glGetString( GL_VERSION )

glEnable( GL_SCISSOR_TEST )
glDisable( GL_CULL_FACE )
glDisable( GL_DEPTH_TEST )

# create a shader
vs = glCreateShader( GL_VERTEX_SHADER )
glShaderSource( vs, vs_source )
glCompileShader( vs )

fs = glCreateShader( GL_FRAGMENT_SHADER )
glShaderSource( fs, fs_source )
glCompileShader( fs )

shader = glCreateProgram()
glAttachShader( shader, vs )
glAttachShader( shader, fs )

# attribute values
glBindAttribLocation( shader, 0, "in_position" )
glBindFragDataLocation( shader, 0, "out_frag_color" )

glLinkProgram( shader )

if not glGetProgramiv( shader, GL_LINK_STATUS ):
    print glGetProgramInfoLog( shader )
    exit()

# create a triangle
vertices = numpy.array(
    [
         1.0, 1.0,-1.0,
        -1.0, 1.0,-1.0,
         1.0, 1.0, 1.0,
        -1.0, 1.0,-1.0,
        -1.0, 1.0, 1.0,
         1.0, 1.0, 1.0,

         1.0,-1.0, 1.0,
        -1.0,-1.0, 1.0,
         1.0,-1.0,-1.0,
        -1.0,-1.0, 1.0,
        -1.0,-1.0,-1.0,
         1.0,-1.0,-1.0,

         1.0, 1.0, 1.0,
        -1.0, 1.0, 1.0,
         1.0,-1.0, 1.0,
        -1.0, 1.0, 1.0,
        -1.0,-1.0, 1.0,
         1.0,-1.0, 1.0,

         1.0,-1.0,-1.0,
        -1.0,-1.0,-1.0,
         1.0, 1.0,-1.0,
        -1.0,-1.0,-1.0,
        -1.0, 1.0,-1.0,
         1.0, 1.0,-1.0,

        -1.0, 1.0, 1.0,
        -1.0, 1.0,-1.0,
        -1.0,-1.0, 1.0,
        -1.0, 1.0,-1.0,
        -1.0,-1.0,-1.0,
        -1.0,-1.0, 1.0,

         1.0, 1.0,-1.0,
         1.0, 1.0, 1.0,
         1.0,-1.0,-1.0,
         1.0, 1.0, 1.0,
         1.0,-1.0, 1.0,
         1.0,-1.0,-1.0
        ],
    dtype = 'float32'
    )

vertices *= 0.5
print vertices

vao = glGenVertexArrays( 1 )
vbo = glGenBuffers( 1 )

glBindVertexArray( vao )

glBindBuffer( GL_ARRAY_BUFFER, vbo )
glBufferData(
    GL_ARRAY_BUFFER,
    vertices.nbytes,
    vertices,
    GL_STATIC_DRAW
    )
glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, 0 )
glEnableVertexAttribArray( 0 )

glBindBuffer( GL_ARRAY_BUFFER, 0 )
glBindVertexArray( 0 )



def on_draw():
    global window
    global shader
    global vao
    global vertices

    width, height = glfw.GetWindowSize()

    class Object( object ):
        pass

    window = Object()
    window.width = width
    window.height = height

    glViewport(0, 0, window.width, window.height)

    #glScissor( 0, 0, window.width, window.height )
    glClearColor( 0.5, 0.5, 0.5, 1.0 )
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

    #glScissor( 0, 0, window.width / 2, window.height / 2 )
    #glClearColor( 0.0, 0.0, 0.0, 1.0 )
    #glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

    #glScissor( 0, 0, window.width, window.height )

    glUseProgram( shader )
    glBindVertexArray( vao )

    glDrawArrays( GL_TRIANGLES, 0, vertices.size / 3 )

    glBindVertexArray( 0 )
    glUseProgram( 0 )

    #assert GL_NO_ERROR == glGetError()

    glFlush()


def run():
    while True:
        if glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS:
            break

        if not glfw.GetWindowParam( glfw.OPENED ):
            break

        on_draw()
        
        glfw.SwapBuffers()



run()

glfw.Terminate()

