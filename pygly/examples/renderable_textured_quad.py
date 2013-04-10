import textwrap

import numpy
from OpenGL import GL

from pygly.shader import Shader, VertexShader, FragmentShader, ShaderProgram
from pygly.dtype_vertex_buffer import DtypeVertexBuffer
from pygly.vertex_array import VertexArray


# create a triangle
vertices = numpy.array(
    [
        #  X    Y    Z          U    V
        (( 1.0, 1.0, 0.0),     (1.0, 1.0)),
        ((-1.0, 1.0, 0.0),     (0.0, 1.0)),
        (( 1.0,-1.0, 0.0),     (1.0, 0.0)),
        ((-1.0, 1.0, 0.0),     (0.0, 1.0)),
        ((-1.0,-1.0, 0.0),     (0.0, 0.0)),
        (( 1.0,-1.0, 0.0),     (1.0, 0.0)),
        ],
    dtype = [
        ('position',        'float32',  (3,)),
        ('texture_coord',   'float32',  (2,)),
        ]
    )


def create( core_profile = True ):
    if core_profile:
        return CoreQuad()
    else:
        return LegacyQuad()


class CoreQuad( object ):

    vertex_shader = textwrap.dedent( """
        #version 150

        // input
        in vec3 in_position;
        in vec2 in_uv;
        uniform mat4 model_view;
        uniform mat4 projection;

        // shared
        out vec2 ex_uv;

        void main(void) 
        {
            // apply projection and model view matrix to vertex
            gl_Position = projection * model_view * vec4( in_position, 1.0 );

            ex_uv = in_uv;
        }
        """ )

    fragment_shader = textwrap.dedent( """
        #version 150

        // shared
        in vec2 ex_uv;
        uniform sampler2D in_diffuse_texture;

        // output
        out vec4 fragColor;

        void main(void) 
        {
            // set colour of each fragment
            fragColor = texture( in_diffuse_texture, ex_uv );
        }
        """ )


    def __init__( self ):
        super( CoreQuad, self ).__init__()

        global vertices

        # create our shader
        self.shader = ShaderProgram(
            VertexShader( self.vertex_shader ),
            FragmentShader( self.fragment_shader )
            )

        # create a vertex buffer
        # we pass in a list of regions we want to define
        # we only have 1 region here
        # for each region, we pass in how many rows, and the dtype
        self.buffer = DtypeVertexBuffer(
            vertices.dtype,
            GL.GL_ARRAY_BUFFER,
            GL.GL_STATIC_DRAW,
            data = vertices
            )

        self.vao = VertexArray()

        # pass the shader and region to our VAO
        # and bind each of the attributes to a VAO index
        # the shader name is the variable name used in the shader
        # the buffer name is the name of the property in our vertex dtype
        # create our vertex array
        self.vao.bind()
        self.buffer.bind()
        self.buffer.set_attribute_pointer_dtype( self.shader, 'in_position', 'position' )
        self.buffer.set_attribute_pointer_dtype( self.shader, 'in_uv', 'texture_coord' )
        self.buffer.unbind()
        self.vao.unbind()

    def draw( self, projection, model_view ):
        self.shader.bind()
        self.shader.uniforms['projection'].value = projection
        self.shader.uniforms['model_view'].value = model_view
        self.shader.uniforms['in_diffuse_texture'].value = 0

        self.vao.bind()
        GL.glDrawArrays( GL.GL_TRIANGLES, 0, self.buffer.rows )
        self.vao.unbind()

        self.shader.unbind()


class LegacyQuad( object ):

    vertex_shader = textwrap.dedent( """
        #version 120

        // input
        attribute vec2 in_uv;

        // shared
        varying vec2 ex_uv;

        void main(void) 
        {
            // apply projection and model view matrix to vertex
            gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;

            ex_uv = in_uv;
        }
        """ )

    fragment_shader = textwrap.dedent( """
        #version 120

        // input
        uniform sampler2D in_diffuse_texture;

        // shared
        varying vec2 ex_uv;

        void main(void) 
        {
            // set colour of each fragment
            gl_FragColor = texture2D( in_diffuse_texture, ex_uv );;
        }
        """ )


    def __init__( self ):
        super( LegacyQuad, self ).__init__()

        global vertices

        self.use_shaders = True

        # create our shader
        self.shader = ShaderProgram(
            VertexShader( self.vertex_shader ),
            FragmentShader( self.fragment_shader )
            )

        # create our vertex buffer
        self.buffer = DtypeVertexBuffer(
            vertices.dtype,
            GL.GL_ARRAY_BUFFER,
            GL.GL_STATIC_DRAW,
            data = vertices
            )

    def draw( self ):
        if self.use_shaders:
            self.shader.bind()

        self.buffer.bind()
        self.buffer.push_attributes()

        # set the vertex pointer to the position data
        self.buffer.set_vertex_pointer_dtype( 'position' )
        self.buffer.set_texture_coord_pointer_dtype( 'texture_coord' )

        GL.glDrawArrays( GL.GL_TRIANGLES, 0, self.buffer.rows )

        self.buffer.pop_attributes()
        self.buffer.unbind()

        if self.use_shaders:
            self.shader.unbind()

