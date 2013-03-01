import numpy
from OpenGL.GL import *

import pygly.shader
from pygly.shader import Shader, ShaderProgram
from pygly.buffer import TypedBuffer, BufferRegion
from pygly.vertex_array import VertexArray


shader_source = {
    'vert': """
#version 150

in  vec3 in_position;
in  vec3 in_colour;
uniform mat4 model_view;
uniform mat4 projection;

out vec3 ex_colour;

void main(void) 
{
    // apply projection and model view matrix to vertex
    gl_Position = projection * model_view * vec4( in_position, 1.0 );

    ex_colour = in_colour;
}
""",

    'frag': """
#version 150

// Video card drivers require this next line to function properly
precision highp float;

in vec3 ex_colour;
out vec4 fragColor;

void main(void) 
{
    // set colour of each fragment
    fragColor = vec4( ex_colour, 1.0 );
}
"""
    }

shader = None
vao = None
vbo = None

# we're going to use the PyGLy VertexArray / Buffer for this code
# we could create the data in the appropriate format to begin with
# but we'll demonstrate how to convert from a flat set of values
# to a more complex dtype

# if we didn't do this, the values would need to be in tuples
# Ie. [ ( (1., 1., 1.), (0., 0., 0.) ), ... ]

# lay out our data as 'position', 'colour'
vertices_simple = numpy.array(
    [
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
         1.0,-1.0,-1.0,     1.0, 0.0, 0.0
        ],
    dtype = 'f4'
     )

# convert to our named view
vertices = vertices_simple.view(
    dtype = [
        ('position',    'float32',  (3,)),
        ('colour',      'float32',  (3,))
        ]
    )


def create():
    global vao
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

    # create a vertex buffer
    # we pass in a list of regions we want to define
    # we only have 1 region here
    # for each region, we pass in how many rows, and the dtype
    vbo = TypedBuffer(
        GL_ARRAY_BUFFER,
        GL_STATIC_DRAW,
        (vertices.size, vertices.dtype)
        )
    print vbo

    # get the created region object
    # this is the first, and only, region was passed in
    vertices_buffer = vbo[ 0 ]

    # pass the data to the region
    vbo.bind()
    vertices_buffer.set_data( vertices )

    # pass the shader and region to our VAO
    # and bind each of the attributes to a VAO index
    # the shader name is the variable name used in the shader
    # the buffer name is the name of the property in our vertex dtype
    # create our vertex array
    vao = VertexArray()
    vao.bind()
    vao.set_buffer_attribute( shader, 'in_position', vertices_buffer, 'position' )
    vao.set_buffer_attribute( shader, 'in_colour', vertices_buffer, 'colour' )
    vao.unbind()

    vbo.unbind()

def draw( projection, model_view ):
    global vao
    global vertices
    global shader

    shader.bind()
    shader.uniforms.model_view = model_view
    shader.uniforms.projection = projection

    vao.bind()
    glDrawArrays( GL_TRIANGLES, 0, vertices.size )
    vao.unbind()

    shader.unbind()

