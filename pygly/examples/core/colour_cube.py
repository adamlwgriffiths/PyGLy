import numpy
from OpenGL.GL import *
from OpenGL.arrays.vbo import VBO
from OpenGL.GL.ARB.vertex_array_object import *

import pygly.gl
from pygly.shader import Shader, ShaderProgram

from ctypes import *


shader_source = {
    'vert': """
#version 150

in  vec3 in_position;
uniform mat4 model_view;
uniform mat4 projection;

void main(void) 
{
    gl_Position = projection * model_view * vec4(
        in_position,
        1.0
        );
}
""",

    'frag': """
#version 150

// Video card drivers require this next line to function properly
precision highp float;

uniform vec4 colour;

out vec4 fragColor;

void main(void) 
{
    //Set colour of each fragment
    fragColor = colour;
}
"""
    }

shader = None
vao = None
vbo = None

vertices = numpy.array([
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
     1.0,-1.0,-1.0,
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
    shader = ShaderProgram(
        False,
        Shader( GL_VERTEX_SHADER, shader_source['vert'] ),
        Shader( GL_FRAGMENT_SHADER, shader_source['frag'] )
        )
    # set our shader data
    # we MUST do this before we link the shader
    shader.attributes.in_position = 0
    shader.frag_location( 'fragColor' )

    # link the shader now
    shader.link()

    # bind our vertex array
    vao = glGenVertexArrays( 1 )
    glBindVertexArray( vao )

    vbo = glGenBuffers( 1 )
    glBindBuffer( GL_ARRAY_BUFFER, vbo )
    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
        )

    # load our vertex positions
    # this will be attribute 0
    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, None )
    glEnableVertexAttribArray( 0 )

    # unbind our buffers
    glBindBuffer( GL_ARRAY_BUFFER, 0 )
    glBindVertexArray( 0 )

    def print_shader_info():
        # print the shader variables we've found via GL calls
        print "Uniforms:"
        for uniform in shader.uniforms.all().values():
            print "%s\t%s" % (uniform.name, uniform.type)
        print "Attributes:"
        for name, type in shader.attributes.all().items():
            print "%s\t%s" % (name, type)
    print_shader_info()


def draw( projection, model_view, colour ):
    global vao
    global vertices
    global shader

    shader.bind()
    shader.uniforms.model_view = model_view
    shader.uniforms.projection = projection
    shader.uniforms.colour = colour

    glBindVertexArray( vao )

    glDrawArrays( GL_TRIANGLES, 0, vertices.size / 3 )

    glBindVertexArray( 0 )
    shader.unbind()

