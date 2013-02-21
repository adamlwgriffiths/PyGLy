from OpenGL.GL import *
import numpy

import pygly.shader
from pygly.shader import Shader, ShaderProgram

from ctypes import *


shader_source = {
    'vert': """
#version 150

in  vec3 in_position;
in  vec2 in_uv;
uniform mat4 in_model_view;
uniform mat4 in_projection;

out vec2 ex_uv;

void main(void) 
{
    gl_Position = in_projection * in_model_view * vec4( in_position, 1.0 );
    ex_uv = in_uv;
}
""",

    'frag': """
#version 150

in vec2 ex_uv;
out vec4 fragColor;

uniform sampler2D in_diffuse_texture;

void main(void) 
{
    //Set colour of each fragment
    fragColor = texture( in_diffuse_texture, ex_uv );
}
"""
    }

shader = None
vao = None
vbo = None

vertices = numpy.array([
     1.0, 1.0, 1.0,     1.0, 1.0,
    -1.0, 1.0, 1.0,     0.0, 1.0,
     1.0,-1.0, 1.0,     1.0, 0.0,
    -1.0, 1.0, 1.0,     0.0, 1.0,
    -1.0,-1.0, 1.0,     0.0, 0.0,
     1.0,-1.0, 1.0,     1.0, 0.0,
     ],
     dtype = 'float32'
     )

def create():
    global vao
    global vbo
    global vertices
    global uvs
    global shader
    global shader_source

    # create our shader but don't link it yet
    shader = ShaderProgram(
        Shader( GL_VERTEX_SHADER, shader_source['vert'] ),
        Shader( GL_FRAGMENT_SHADER, shader_source['frag'] ),
        link_now = False
        )
    # set our shader data
    # we MUST do this before we link the shader
    shader.attributes.in_position = 0
    shader.attributes.in_uv = 1

    shader.frag_location( 'fragColor' )

    # link the shader now
    shader.link()

    print shader
    
    # set our diffuse texture stage
    # do this now as the value doesn't change
    shader.bind()
    #shader.uniforms.in_diffuse_texture = 0
    shader.unbind()

    for uniform in pygly.shader.uniforms(shader.handle):
        print uniform

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
    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 5 * 4, None )
    glEnableVertexAttribArray( 0 )

    # load our texture coordinates
    # this will be attribute 1
    glVertexAttribPointer( 1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4) )
    glEnableVertexAttribArray( 1 )

    # unbind our buffers
    glBindBuffer( GL_ARRAY_BUFFER, 0 )
    glBindVertexArray( 0 )

    print shader

def draw( projection, model_view ):
    global vao
    global vertices
    global shader

    shader.bind()
    shader.uniforms.in_model_view = model_view
    shader.uniforms.in_projection = projection

    glBindVertexArray( vao )

    glDrawArrays( GL_TRIANGLES, 0, vertices.size / 3 )

    glBindVertexArray( 0 )
    shader.unbind()

