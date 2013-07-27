import textwrap

import numpy
from OpenGL import GL

from pygly.shader import Shader, VertexShader, FragmentShader, ShaderProgram
from pygly.vertex_buffer import VertexBuffer, BufferAttributes, GenericAttribute, VertexAttribute, TextureCoordAttribute
from pygly.vertex_array import VertexArray
from pyrr import geometry


vertices, indices = geometry.create_quad(scale=(5.0,5.0), st=True, dtype='float32')
vertices = vertices[indices]
vertices.dtype = [
    ('position',        'float32',  (3,)),
    ('texture_coord',   'float32',  (2,)),
]


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
        self.buffer = VertexBuffer(
            GL.GL_ARRAY_BUFFER,
            GL.GL_STATIC_DRAW,
            data = vertices,
            )

        # pass the shader and region to our VAO
        # and bind each of the attributes to a VAO index
        # the shader name is the variable name used in the shader
        # the buffer name is the name of the property in our vertex dtype
        self.buffer_attributes = BufferAttributes()
        self.buffer_attributes[ 'position' ] = GenericAttribute.from_dtype(
            self.buffer,
            vertices.dtype,
            'position',
            location = self.shader.attributes[ 'in_position' ]
            )
        self.buffer_attributes[ 'uv' ] = GenericAttribute.from_dtype(
            self.buffer,
            vertices.dtype,
            'texture_coord',
            location = self.shader.attributes[ 'in_uv' ]
            )

        # create our vertex array
        self.vao = VertexArray()

        self.vao.bind()
        self.buffer.bind()
        self.buffer_attributes.set()
        self.buffer.unbind()
        self.vao.unbind()

        #self.buffer['position'] = self.shader['in_position']

    def draw( self, projection, model_view ):
        global vertices

        self.shader.bind()
        self.shader.uniforms[ 'projection' ].value = projection
        self.shader.uniforms[ 'model_view' ].value = model_view
        self.shader.uniforms[ 'in_diffuse_texture' ].value = 0

        self.vao.bind()
        GL.glDrawArrays( GL.GL_TRIANGLES, 0, len( vertices ) )
        self.vao.unbind()

        self.shader.unbind()


class LegacyQuad( object ):

    vertex_shader = textwrap.dedent( """
        #version 120

        void main(void) 
        {
            // apply projection and model view matrix to vertex
            gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;

            // select the texture coordinate to use
            gl_TexCoord[0]  = gl_MultiTexCoord0;
        }
        """ )

    fragment_shader = textwrap.dedent( """
        #version 120

        // input
        uniform sampler2D in_diffuse_texture;

        void main(void) 
        {
            // set colour of each fragment
            gl_FragColor = texture2D( in_diffuse_texture, gl_TexCoord[0].st );
        }
        """ )


    def __init__( self ):
        super( LegacyQuad, self ).__init__()

        global vertices

        self.use_shaders = True

        GL.glEnable(GL.GL_TEXTURE_2D)

        # create our shader
        self.shader = ShaderProgram(
            VertexShader( self.vertex_shader ),
            FragmentShader( self.fragment_shader )
            )

        # create our vertex buffer
        self.buffer = VertexBuffer(
            GL.GL_ARRAY_BUFFER,
            GL.GL_STATIC_DRAW,
            data = vertices,
            )

        self.buffer_attributes = BufferAttributes()
        self.buffer_attributes[ 'position' ] = VertexAttribute.from_dtype(
            self.buffer,
            vertices.dtype,
            'position'
            )

        self.buffer_attributes[ 'uv' ] = TextureCoordAttribute.from_dtype(
            self.buffer,
            vertices.dtype,
            'texture_coord'
            )

    def draw( self ):
        global vertices

        if self.use_shaders:
            self.shader.bind()
            self.shader.uniforms[ 'in_diffuse_texture' ].value = 0

        self.buffer_attributes.push_attributes()

        # set the vertex pointer to the position data
        self.buffer.bind()
        self.buffer_attributes.set()
        self.buffer.unbind()

        GL.glDrawArrays( GL.GL_TRIANGLES, 0, len( vertices ) )

        self.buffer_attributes.pop_attributes()

        if self.use_shaders:
            self.shader.unbind()

