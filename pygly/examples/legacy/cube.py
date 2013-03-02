import numpy
from OpenGL.GL import *

from pygly.buffer import TypedBuffer, BufferRegion

vbo = None

vertices_simple = numpy.array([
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

# convert to our named view
vertices = vertices_simple.view(
    dtype = [
        ('position',    'float32',  (3,)),
        ('colour',      'float32',  (3,))
        ]
    )

def create():
    # TODO: convert this to a display list
    global vbo
    global vertices

    vbo = TypedBuffer(
        GL_ARRAY_BUFFER,
        GL_STATIC_DRAW,
        (vertices.size, vertices.dtype)
        )
    print vbo

    vertices_buffer = vbo[ 0 ]

    vbo.bind()
    vertices_buffer.set_data( vertices )
    vbo.unbind()

def draw():
    global vbo
    global vertices

    vbo.bind()

    # get the vertices buffer
    vertices_buffer = vbo[ 0 ]

    vertices_buffer.vertex_pointer( 'position' )
    vertices_buffer.color_pointer( 'colour' )

    glDrawArrays( GL_TRIANGLES, 0, vertices.size )

    vbo.unbind()

