import numpy
from OpenGL.GL import *
from OpenGL.arrays.vbo import VBO
from OpenGL.GL.ARB.vertex_array_object import *

from pygly.shader import Shader, ShaderProgram


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
    shader = ShaderProgram(
        False,
        Shader( GL_VERTEX_SHADER, shader_source['vert'] ),
        Shader( GL_FRAGMENT_SHADER, shader_source['frag'] ),
        )
    # set our shader data
    # we MUST do this before we link the shader
    shader.attributes.in_position = 0
    shader.attributes.in_colour = 1
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
    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 6 * 4, None )
    glEnableVertexAttribArray( 0 )

    # load our vertex colours
    # this will be attribute 1
    glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4) )
    glEnableVertexAttribArray( 1 )

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

def draw( projection, model_view ):
    global vao
    global vertices
    global shader

    shader.bind()
    shader.uniforms.model_view = model_view
    shader.uniforms.projection = projection

    glBindVertexArray( vao )
    glDrawArrays( GL_TRIANGLES, 0, vertices.size / 3 )
    glBindVertexArray( 0 )

    shader.unbind()

