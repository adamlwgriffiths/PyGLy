import ctypes

from OpenGL import GL


class VertexArray( object ):
    """Wraps OpenGL Vertex Array Objects.

    Provides wrappers around standard functions and higher level
    wrappers with PyGLy.BufferRegion interfaces.

    Example::
    
        vs = Shader( GL_VERTEX_SHADER, shader_source['vert'] )
        fs = Shader( GL_FRAGMENT_SHADER, shader_source['frag'] )
        shader = ShaderProgram( vs, fs )

        # a basic triangle
        vertices = numpy.array(
            [
                #  X    Y    Z          R    G    B
                (( 0.0, 1.0, 0.0),     (1.0, 0.0, 0.0)),
                ((-2.0,-1.0, 0.0),     (0.0, 1.0, 0.0)),
                (( 2.0,-1.0, 0.0),     (0.0, 0.0, 1.0)),
                ],
            dtype = [
                ('position','float32',(3,)),
                ('colour','float32',(3,))
                ]
            )
        buffer = DtypeVertexBuffer(
            vertices.dtype,
            GL_ARRAY_BUFFER,
            GL_STATIC_DRAW,
            data = vertices
            )

        vao = VertexArray()

        vao.bind()
        buffer.bind()
        buffer.set_attribute_pointer_dtype( shader, 'in_position', 'position' )
        buffer.set_attribute_pointer_dtype( shader, 'in_colour', 'colour' )
        buffer.unbind()
        vao.unbind()

    .. warning:: This is an OpenGL Core function (>=3.0) and should not be
        called for Legacy profile applications (<=2.1).
    """

    def __init__( self ):
        super( VertexArray, self ).__init__()

        self._handle = GL.glGenVertexArrays( 1 )

    @property
    def handle( self ):
        return self._handle

    def bind( self ):
        GL.glBindVertexArray( self.handle )

    def unbind( self ):
        GL.glBindVertexArray( 0 )

