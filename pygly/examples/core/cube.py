import numpy
from OpenGL.GL import *

import pygly.shader
from pygly.shader import Shader, ShaderProgram
from pygly.buffer import Buffer
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
    gl_Position = projection * model_view * vec4(
        in_position,
        1.0
        );

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
    //Set colour of each fragment
    fragColor = vec4( ex_colour, 1.0 );
}
"""
    }

shader = None
vao = None
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
    shader = ShaderProgram( vs, fs, link_now = False )

    # set our shader data
    # we MUST do this before we link the shader
    shader.frag_location( 'fragColor' )
    shader.link()

    # bind our vertex array
    vao = VertexArray()
    vao.bind()

    vbo = Buffer( GL_ARRAY_BUFFER, GL_STATIC_DRAW )
    vbo.bind()
    vbo.set_data( vertices )

    # load our vertex positions
    # this will be attribute 0
    vao.set_attribute(
        shader.attributes.in_position.location,
        3,
        GL_FLOAT,
        stride = 6 * 4,
        offset = 0,
        normalise = False
        )
    vao.enable_attribute( shader.attributes.in_position.location )

    # load our vertex colours
    # this will be attribute 1
    vao.set_attribute(
        shader.attributes.in_colour.location,
        3,
        GL_FLOAT,
        stride = 6 * 4,
        offset = 3 * 4,
        normalise = False
        )
    vao.enable_attribute( shader.attributes.in_colour.location )

    # unbind our buffers
    vbo.unbind()
    vao.unbind()

    # print out our shader description
    print shader

def draw( projection, model_view ):
    global vao
    global vertices
    global shader

    shader.bind()
    shader.uniforms.model_view = model_view
    shader.uniforms.projection = projection

    vao.bind()
    glDrawArrays( GL_TRIANGLES, 0, vertices.size / 3 )
    vao.unbind()

    shader.unbind()

