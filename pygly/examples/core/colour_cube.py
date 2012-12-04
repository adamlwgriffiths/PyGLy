import pyglet.graphics
from pyglet.gl import *

from pygly.shader import Shader, ShaderProgram
import cube

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

vao = None
vbo = None


def create():
    global vao
    global vbo
    global vertices
    global colours
    global shader
    global shader_source

    # create our shader but don't link it yet
    shader = ShaderProgram(
        False,
        Shader( GL_VERTEX_SHADER, shader_source['vert'] ),
        Shader( GL_FRAGMENT_SHADER, shader_source['frag'] ),
        )
    # set our shader data
    # we MUST do this before we link the shader
    shader.attributes.in_position = 0
    shader.frag_location( 'fragColor' )

    # link the shader now
    shader.link()

    vao = (GLuint)()
    glGenVertexArrays( 1, vao )

    vbo = (GLuint * 1)()
    glGenBuffers( 1, vbo )

    # bind our vertex array
    glBindVertexArray( vao )

    # load our vertex positions
    # this will be attribute 0
    glBindBuffer( GL_ARRAY_BUFFER, vbo[ 0 ] )
    glBufferData(
        GL_ARRAY_BUFFER,
        cube.vertices.nbytes,
        (GLfloat * cube.vertices.size)(*cube.vertices),
        GL_STATIC_DRAW
        )
    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, 0)
    glEnableVertexAttribArray( 0 )

    # unbind our buffers
    glBindVertexArray( 0 )


def draw( projection, model_view, colour ):
    global vao
    global vertices
    global shader

    shader.bind()
    shader.uniforms.model_view = model_view
    shader.uniforms.projection = projection
    shader.uniforms.colour = colour

    glBindVertexArray( vao )

    glDrawArrays( GL_TRIANGLES, 0, cube.vertices.size / 3 )

    glBindVertexArray( 0 )
    shader.unbind()

