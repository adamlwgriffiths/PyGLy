import textwrap

import numpy
from OpenGL import GL

from pygly.shader import Shader, ShaderProgram
from pygly.dtype_vertex_buffer import DtypeVertexBuffer
from pygly.vertex_array import VertexArray


vertices = numpy.array(
    [
        (( 1.0, 1.0,-1.0),),
        ((-1.0, 1.0,-1.0),),
        (( 1.0, 1.0, 1.0),),
        ((-1.0, 1.0,-1.0),),
        ((-1.0, 1.0, 1.0),),
        (( 1.0, 1.0, 1.0),),

        (( 1.0,-1.0, 1.0),),
        ((-1.0,-1.0, 1.0),),
        (( 1.0,-1.0,-1.0),),
        ((-1.0,-1.0, 1.0),),
        ((-1.0,-1.0,-1.0),),
        (( 1.0,-1.0,-1.0),),

        (( 1.0, 1.0, 1.0),),
        ((-1.0, 1.0, 1.0),),
        (( 1.0,-1.0, 1.0),),
        ((-1.0, 1.0, 1.0),),
        ((-1.0,-1.0, 1.0),),
        (( 1.0,-1.0, 1.0),),

        (( 1.0,-1.0,-1.0),),
        ((-1.0,-1.0,-1.0),),
        (( 1.0, 1.0,-1.0),),
        ((-1.0,-1.0,-1.0),),
        ((-1.0, 1.0,-1.0),),
        (( 1.0, 1.0,-1.0),),

        ((-1.0, 1.0, 1.0),),
        ((-1.0, 1.0,-1.0),),
        ((-1.0,-1.0, 1.0),),
        ((-1.0, 1.0,-1.0),),
        ((-1.0,-1.0,-1.0),),
        ((-1.0,-1.0, 1.0),),

        (( 1.0, 1.0,-1.0),),
        (( 1.0, 1.0, 1.0),),
        (( 1.0,-1.0,-1.0),),
        (( 1.0, 1.0, 1.0),),
        (( 1.0,-1.0, 1.0),),
        (( 1.0,-1.0,-1.0),),
        ],
    dtype = [
        ('position',    'float32',  (3,)),
        ]
    )


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
            Shader( GL.GL_VERTEX_SHADER, self.vertex_shader ),
            Shader( GL.GL_FRAGMENT_SHADER, self.fragment_shader )
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
        self.buffer.unbind()
        self.vao.unbind()

    def draw( self, projection, model_view, colour ):
        self.shader.bind()
        self.shader.uniforms.projection = projection
        self.shader.uniforms.model_view = model_view
        self.shader.uniforms.in_colour = colour

        self.vao.bind()
        GL.glDrawArrays( GL.GL_TRIANGLES, 0, self.buffer.rows )
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
            Shader( GL.GL_VERTEX_SHADER, self.vertex_shader ),
            Shader( GL.GL_FRAGMENT_SHADER, self.fragment_shader )
            )

        # create our vertex buffer
        self.buffer = DtypeVertexBuffer(
            vertices.dtype,
            GL.GL_ARRAY_BUFFER,
            GL.GL_STATIC_DRAW,
            data = vertices
            )

    def draw( self, colour ):
        if self.use_shaders:
            self.shader.bind()

        self.buffer.bind()
        self.buffer.push_attributes()

        # set the gl colour
        GL.glColor4f( *colour )

        # set the vertex pointer to the position data
        self.buffer.set_vertex_pointer_dtype( 'position' )

        GL.glDrawArrays( GL.GL_TRIANGLES, 0, self.buffer.rows )

        self.buffer.pop_attributes()
        self.buffer.unbind()

        if self.use_shaders:
            self.shader.unbind()

