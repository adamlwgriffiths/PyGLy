import numpy
from OpenGL.GL import *

from pygly.shader import Shader, ShaderProgram
from pygly.buffer import Buffer, BufferRegion


shader_source = {
    'vert': """
#version 120

// we could receive the colour as the 'gl_Color' built in
// but we'll demonstrate attributes by passing it in manually
attribute vec3 in_colour;

varying vec3 ex_colour;

void main(void) 
{
    // apply projection and model view matrix to vertex
    gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;

    ex_colour = in_colour;
}
""",

    'frag': """
#version 120

varying vec3 ex_colour;

void main(void) 
{
    // set colour of each fragment
    gl_FragColor = vec4( ex_colour, 1.0 );
}
"""
    }

shader = None
vbo = None

# we're going to use the PyGLy Buffer for this code
# we could create the data in the appropriate format to begin with
# but we'll demonstrate how to convert from a flat set of values
# to a more complex dtype

# if we didn't do this, the values would need to be in tuples
# Ie. [ ( (1., 1., 1.), (0., 0., 0.) ), ... ]

# lay out our data as 'position', 'colour'
vertices_simple = numpy.array(
    [
        #  X,   Y,   Z,       R,   G,   B,
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
    global shader
    global shader_source

    # create our shader but don't link it yet
    vs = Shader( GL_VERTEX_SHADER, shader_source['vert'] )
    fs = Shader( GL_FRAGMENT_SHADER, shader_source['frag'] )
    print vs
    print fs
    shader = ShaderProgram( vs, fs )
    # print out our shader description
    print shader

    vbo = Buffer(
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
    global shader

    shader.bind()
    vbo.bind()

    # get the vertices buffer
    vertices_buffer = vbo[ 0 ]
    vertices_buffer.vertex_pointer( 'position' )
    # we could use 'vertices_buffer.color_pointer( 'colour' )' to pass
    # the colour value to the shader, but instead we will use a vertex
    # attribute to demonstrate how they are used
    #vertices_buffer.color_pointer( 'colour' )
    vertices_buffer.attribute_pointer( shader, 'in_colour', 'colour' )

    glDrawArrays( GL_TRIANGLES, 0, vertices.size )

    vbo.unbind()
    shader.unbind()
