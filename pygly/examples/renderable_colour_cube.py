import textwrap

import numpy
from OpenGL import GL

from pygly.shader import Shader, VertexShader, FragmentShader, ShaderProgram
from pygly.vertex_buffer import VertexBuffer, BufferAttributes, GenericAttribute, VertexAttribute
from pygly.vertex_array import VertexArray
from pyrr import geometry


vertices, indices = geometry.create_cube(scale=(2.0,2.0,2.0), dtype='float32')
vertices = vertices[indices]
vertices.dtype = [('position', 'float32', (3,)),]


def create( core_profile = True ):
    if core_profile:
        return CoreColourCube()
    else:
        return LegacyColourCube()


class CoreColourCube( object ):

    vertex_shader = textwrap.dedent( """
        #version 150

        // input
        in vec3 in_position;
        uniform mat4 model_view;
        uniform mat4 projection;

        void main(void) 
        {
            // apply projection and model view matrix to vertex
            gl_Position = projection * model_view * vec4( in_position, 1.0 );
        }
        """ )

    fragment_shader = textwrap.dedent( """
        #version 150

        // input
        uniform vec4 in_colour;

        // output
        out vec4 fragColor;

        void main(void) 
        {
            // set colour of each fragment
            fragColor = in_colour;
        }
        """ )


    def __init__( self ):
        super( CoreColourCube, self ).__init__()

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

        # create our vertex array
        self.vao = VertexArray()

        self.vao.bind()
        self.buffer.bind()
        self.buffer_attributes.set()
        self.buffer.unbind()
        self.vao.unbind()

    def draw( self, projection, model_view, colour ):
        self.shader.bind()
        self.shader.uniforms[ 'projection' ].value = projection
        self.shader.uniforms[ 'model_view' ].value = model_view
        self.shader.uniforms[ 'in_colour' ].value = colour

        self.vao.bind()
        GL.glDrawArrays( GL.GL_TRIANGLES, 0, len( vertices ) )
        self.vao.unbind()

        self.shader.unbind()


class LegacyColourCube( object ):

    vertex_shader = textwrap.dedent( """
        #version 120

        void main(void) 
        {
            // apply projection and model view matrix to vertex
            gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;

            gl_FrontColor = gl_Color;
        }
        """ )

    fragment_shader = textwrap.dedent( """
        #version 120

        void main(void) 
        {
            // set colour of each fragment
            gl_FragColor = gl_Color;
        }
        """ )


    def __init__( self ):
        super( LegacyColourCube, self ).__init__()

        global vertices

        self.use_shaders = True

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

    def draw( self, colour ):
        if self.use_shaders:
            self.shader.bind()

        self.buffer_attributes.push_attributes()

        # set the gl colour
        GL.glColor4f( *colour )

        # set the vertex pointer to the position data
        self.buffer.bind()
        self.buffer_attributes.set()
        self.buffer.unbind()

        GL.glDrawArrays( GL.GL_TRIANGLES, 0, len( vertices ) )

        self.buffer_attributes.pop_attributes()

        if self.use_shaders:
            self.shader.unbind()

