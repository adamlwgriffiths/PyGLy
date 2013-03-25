import ctypes

from OpenGL import GL


class VertexArray( object ):
    """Wraps OpenGL Vertex Array Objects.

    This is an OpenGL Core function (>=3.0) and should not be
    called for Legacy profile applications (<=2.1).

    Provides wrappers around standard functions and higher level
    wrappers with PyGLy.BufferRegion interfaces.

    Example::
    
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

