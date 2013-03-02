from OpenGL import GL
import ctypes

from pygly import gl_utils


class VertexArray( object ):
    """Wraps OpenGL Vertex Array Objects.

    This is an OpenGL Core function (>=3.0) and should not be
    called for Legacy profile applications (<=2.1).

    Provides wrappers around standard functions and higher level
    wrappers with PyGLy.BufferRegion interfaces.

    Example:
    vs = Shader( GL_VERTEX_SHADER, shader_source['vert'] )
    fs = Shader( GL_FRAGMENT_SHADER, shader_source['frag'] )
    shader = ShaderProgram( vs, fs )

    vertices = numpy.array(
        [ ... ],
        dtype = [
            ('position','float32',(3,)),
            ('normal','float32',(3,))
            ]
        )
    vbo = Buffer(
        GL_ARRAY_BUFFER,
        GL_STATIC_DRAW,
        (vertices.size, vertices.dtype)
        )
    vbo.bind()
    vertices_buffer.set_data( vertices )

    vao = VertexArray()
    vao.bind()
    vao.set_attribute( shader, 'in_position', vertices_buffer, 'position' )
    vao.set_attribute( shader, 'in_normal', vertices_buffer, 'normal' )
    vao.unbind()

    vbo.unbind()
    """

    def __init__(
        self,
        target = GL.GL_ARRAY_BUFFER,
        usage = GL.GL_STATIC_DRAW
        ):
        super( VertexArray, self ).__init__()

        self._handle = GL.glGenVertexArrays( 1 )

    @property
    def handle( self ):
        return self._handle

    @property
    def is_bound( self ):
        pass

    def bind( self ):
        GL.glBindVertexArray( self.handle )

    def unbind( self ):
        GL.glBindVertexArray( 0 )

    def enable_shader_attribute( self, shader, attribute ):
        location = shader.attributes[ attribute ]
        self.enable_attribute( location )

    def disable_shader_attribute( self, shader, attribute ):
        location = shader.attributes[ attribute ]
        self.disable_attribute( location )

    def enable_attribute( self, index ):
        GL.glEnableVertexAttribArray( index )

    def disable_attribute( self, index ):
        GL.glDisableVertexAttribArray( index )

    def set_attribute(
        self,
        location,
        values_per_vertex,
        glType,
        stride,
        offset,
        normalise = False,
        enable = True
        ):
        if offset == 0:
            offset = None
        else:
            offset = ctypes.c_void_p( offset )

        if enable:
            self.enable_attribute( location )

        GL.glVertexAttribPointer(
            location,
            values_per_vertex,
            glType,
            GL.GL_TRUE if normalise else GL.GL_FALSE,
            stride,
            offset
            )

    def set_buffer_attribute(
        self,
        shader,
        attribute,
        buffer_region,
        name = None,
        normalise = False,
        enable = True
        ):
        """Binds the attribute to the currently bound buffer.

        This method wraps the glVertexAttribPointer call using
        information provided by the shader object and the BufferRegion
        object.

        shader is a PyGLy ShaderProgram object.
        attribute is the name of a shader attribute variable.
        buffer_region is a PyGLy BufferRegion object created from a
        PyGLy Buffer.
        name is the column name in the BufferRegion dtype.

        For example:
        vao.set_buffer_attribute( shader, 'in_position', vertices_buffer, 'position' )
        """
        # get the attribute location
        location = shader.attributes[ attribute ].location

        values_per_vertex = buffer_region.element_count( name )
        glType = buffer_region.type( name )
        stride = buffer_region.stride
        offset = buffer_region.offset( name )

        self.set_attribute(
            location,
            values_per_vertex,
            glType,
            stride,
            offset,
            normalise,
            enable
            )
