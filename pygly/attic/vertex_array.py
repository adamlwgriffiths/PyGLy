from pygly.vertex_buffer import VertexBuffer


class VertexArray( object ):

    attrib_pointer_function = {
        GL_BYTE:            glVertexAttribPointerI,
        GL_UNSIGNED_BYTE:   glVertexAttribPointerI,
        GL_SHORT:           glVertexAttribPointerI,
        GL_UNSIGNED_SHORT:  glVertexAttribPointerI,
        GL_INT:             glVertexAttribPointerI,
        GL_UNSIGNED_INT:    glVertexAttribPointerI,
        GL_HALF_FLOAT:      glVertexAttribPointer,
        GL_FLOAT:           glVertexAttribPointer,
        GL_DOUBLE:          glVertexAttribPointerL,
        }

    def __init__( self ):
        super( VertexArray, self ).__init__()

        self.id = (GLuint)()
        glGenVertexArrays( 1, self.id )

    def __del__( self ):
        id = getattr( self, 'id', None )
        if id and id.value != 0:
            glDeleteVertexArrays( 1, id )

    def bind( self ):
        glBindVertexArray( self.id )

    def unbind( self ):
        glBindVertexArray( 0 )

    def set_vertex_buffer( self, size, type, stride, offset ):
        pointer = (GLvoid)( sizeof(gl_type) * offset )
        glVertexPointer( size, type, stride, pointer )

    def set_normal_buffer( self, size, stride, offset ):
        pointer = (GLvoid)( sizeof(gl_type) * offset )
        glNormalPointer( size, stride, pointer )

    def set_colour_buffer( self, size, type, stride, offset ):
        pointer = (GLvoid)( sizeof(gl_type) * offset )
        glColourPointer( size, type, stride, pointer )

    def set_texture_coordinate_buffer( self, size, type, stride, offset ):
        pointer = (GLvoid)( sizeof(gl_type) * offset )
        glTexCoordPointer( size, type, stride, pointer )

    def set_buffer( self, index, buffer, normalise = False, stride = 0, offset = 0 ):
        type_tuple, element_size, usage = VertexBuffer.parse_format( format )

        # extract the gl type enum and data type
        gl_enum, gl_type = type_tuple

        gl_normalise = GL_TRUE if normalise else GL_FALSE

        # convert our offset to a pointer
        # because it's a pointer, it needs to be converted from
        # element offset to memory offset
        pointer = (GLvoid)( sizeof(gl_type) * offset )

        func = VertexArray.attrib_pointer_function[ gl_enum ]

        func(
            index,
            element_size,
            gl_enum,
            gl_normalise,
            stride,
            pointer
            )

