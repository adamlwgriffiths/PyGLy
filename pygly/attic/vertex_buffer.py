from ctypes import *

from pyglet.gl import *

import pygly.utils


class VertexBuffer( object ):

    # http://www.khronos.org/files/opengl-quick-reference-card.pdf
    types = {
        'i8':       (GL_BYTE, GLbyte),
        'u8':       (GL_UNSIGNED_BYTE, GLubyte),
        'i16':      (GL_SHORT, GLshort),
        'u16':      (GL_UNSIGNED_SHORT, GLushort),
        'i32':      (GL_INT, GLint),
        'u32':      (GL_UNSIGNED_INT, GLuint),
        # no native half-float
        'f16':      (GL_HALF_FLOAT, GLfloat),
        'f32':      (GL_FLOAT, GLfloat),
        'f64':      (GL_DOUBLE, GLdouble),
        }

    uses = {
        'stream_draw':  GL_STREAM_DRAW,
        'stream_read':  GL_STREAM_READ,
        'stream_copy':  GL_STREAM_COPY,
        'static_draw':  GL_STATIC_DRAW,
        'static_read':  GL_STATIC_READ,
        'static_copy':  GL_STATIC_COPY,
        'dynamic_draw': GL_DYNAMIC_DRAW,
        'dynamic_read': GL_DYNAMIC_READ,
        'dynamic_copy': GL_DYNAMIC_COPY,
        }

    @staticmethod
    def parse_format( format ):
        values = format.split('/')
        type, element_size, usage = pygly.utils.extract_tuple( values, 3 )

        return(
            VertexBuffer.types[ type ],
            int( element_size ),
            VertexBuffer.uses[ usage ]
            )

    def __init__( self, target = GL_ARRAY_BUFFER ):
        super( VertexBuffer, self ).__init__()

        self.id = (GLuint)()
        glGenBuffers( 1, self.id )

        self.target = target

        self.format = ''

    def __del__( self ):
        id = getattr( self, 'id', None )
        if id and id.value != 0:
            glDeleteBuffers( 1, id )

    def bind( self ):
        glBindBuffer( self.target, self.id )

    def unbind( self ):
        glBindBuffer( self.target, 0 )

    def set_data( self, format, num_elements, data ):
        """
        Format is as follows:
        data type / values per element / usage

        For example:
        f32/3/static_draw
        """
        # store our format for later
        self.format = format

        type_tuple, element_size, usage = VertexBuffer.parse_format( format )

        # extract the gl type enum and data type
        gl_enum, gl_type = type_tuple

        glBufferData(
            self.target,
            len(data) * sizeof( gl_type ),
            (gl_type * len(data))(*data),
            usage
            )

