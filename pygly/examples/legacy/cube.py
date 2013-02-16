import numpy
from OpenGL.GL import *
from OpenGL.arrays.vbo import VBO
from OpenGL.GL.ARB.vertex_array_object import *

vbo = None

vertices = numpy.array([
     1.0, 1.0,-1.0,     0.0, 1.0, 0.0,
    -1.0, 1.0,-1.0,     0.0, 1.0, 0.0,
     1.0, 1.0, 1.0,     0.0, 1.0, 0.0,
    -1.0, 1.0,-1.0,     0.0, 1.0, 0.0,
    -1.0, 1.0, 1.0,     0.0, 1.0, 0.0,
     1.0, 1.0, 1.0,     0.0, 1.0, 0.0,

     1.0,-1.0, 1.0,     1.0, 0.5, 0.0,
    -1.0,-1.0, 1.0,     1.0, 0.5, 0.0,
     1.0,-1.0,-1.0,     1.0, 0.5, 0.0,
    -1.0,-1.0, 1.0,     1.0, 0.5, 0.0,
    -1.0,-1.0,-1.0,     1.0, 0.5, 0.0,
     1.0,-1.0,-1.0,     1.0, 0.5, 0.0,

     1.0, 1.0, 1.0,     0.0, 0.0, 1.0,
    -1.0, 1.0, 1.0,     0.0, 0.0, 1.0,
     1.0,-1.0, 1.0,     0.0, 0.0, 1.0,
    -1.0, 1.0, 1.0,     0.0, 0.0, 1.0,
    -1.0,-1.0, 1.0,     0.0, 0.0, 1.0,
     1.0,-1.0, 1.0,     0.0, 0.0, 1.0,

     1.0,-1.0,-1.0,     1.0, 0.0, 1.0,
    -1.0,-1.0,-1.0,     1.0, 0.0, 1.0,
     1.0, 1.0,-1.0,     1.0, 0.0, 1.0,
    -1.0,-1.0,-1.0,     1.0, 0.0, 1.0,
    -1.0, 1.0,-1.0,     1.0, 0.0, 1.0,
     1.0, 1.0,-1.0,     1.0, 0.0, 1.0,

    -1.0, 1.0, 1.0,     1.0, 1.0, 0.0,
    -1.0, 1.0,-1.0,     1.0, 1.0, 0.0,
    -1.0,-1.0, 1.0,     1.0, 1.0, 0.0,
    -1.0, 1.0,-1.0,     1.0, 1.0, 0.0,
    -1.0,-1.0,-1.0,     1.0, 1.0, 0.0,
    -1.0,-1.0, 1.0,     1.0, 1.0, 0.0,

     1.0, 1.0,-1.0,     1.0, 0.0, 0.0,
     1.0, 1.0, 1.0,     1.0, 0.0, 0.0,
     1.0,-1.0,-1.0,     1.0, 0.0, 0.0,
     1.0, 1.0, 1.0,     1.0, 0.0, 0.0,
     1.0,-1.0, 1.0,     1.0, 0.0, 0.0,
     1.0,-1.0,-1.0,     1.0, 0.0, 0.0,
     ],
     dtype = 'float32'
     )



def create():
    # TODO: convert this to a display list
    global vbo
    global vertices

    vbo = glGenBuffers( 1 )
    glBindBuffer( GL_ARRAY_BUFFER, vbo )
    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
        )

    # unbind our buffers
    glBindBuffer( GL_ARRAY_BUFFER, 0 )

def draw():
    global vbo
    global vertices

    glBindBuffer( GL_ARRAY_BUFFER, vbo )
    # vertices
    glEnableClientState( GL_VERTEX_ARRAY )
    glVertexPointer( 3, GL_FLOAT, 6 * 4, None )
    # colours
    glEnableClientState( GL_COLOR_ARRAY )
    glColorPointer( 3, GL_FLOAT, 6 * 4, ctypes.c_void_p(3 * 4) )

    glDrawArrays( GL_TRIANGLES, 0, vertices.size / 3 )

    glBindBuffer( GL_ARRAY_BUFFER, 0 )

