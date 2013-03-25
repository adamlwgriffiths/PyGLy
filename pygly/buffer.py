"""
TODO: get gl buffer limit values
"""

import ctypes

from OpenGL import GL

from pyrr.utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays

from pygly import numpy_utils


def currently_bound_buffer( type ):
    if type == GL.GL_TEXTURE_BUFFER:
        enum = GL.GL_TEXTURE_BUFFER_BINDING
    elif type == GL.GL_ELEMENT_ARRAY_BUFFER:
        enum = GL.GL_ELEMENT_ARRAY_BUFFER_BINDING
    else:
        enum = GL.GL_ARRAY_BUFFER_BINDING

    return GL.glGetInteger( enum )

def set_vertex_pointer( values_per_vertex, glType, stride, offset):
    """Sets the glVertexPointer.

    This is an OpenGL Legacy function (<=2.1) and should not be
    called for Core profile applications (>=3.0).
    """
    offset = None if offset == 0 else ctypes.c_void_p( offset )
    GL.glVertexPointer( values_per_vertex, glType, stride, offset )

def set_color_pointer( values_per_vertex, glType, stride, offset ):
    """Sets the glColorPointer.

    This is an OpenGL Legacy function (<=2.1) and should not be
    called for Core profile applications (>=3.0).
    """
    offset = None if offset == 0 else ctypes.c_void_p( offset )
    GL.glColorPointer( values_per_vertex, glType, stride, offset )

def set_texture_coord_pointer( values_per_vertex, glType, stride, offset ):
    """Sets the glTexCoordPointer.

    This is an OpenGL Legacy function (<=2.1) and should not be
    called for Core profile applications (>=3.0).
    """
    offset = None if offset == 0 else ctypes.c_void_p( offset )
    GL.glTexCoordPointer( values_per_vertex, glType, stride, offset )

def set_normal_pointer( glType, stride, offset ):
    """Sets the glNormalPointer.

    This is an OpenGL Legacy function (<=2.1) and should not be
    called for Core profile applications (>=3.0).
    """
    offset = None if offset == 0 else ctypes.c_void_p( offset )
    GL.glNormalPointer( glType, stride, offset )

def set_index_pointer( glType, stride, offset ):
    """Sets the glIndexPointer.

    This is an OpenGL Legacy function (<=2.1) and should not be
    called for Core profile applications (>=3.0).
    """
    offset = None if offset == 0 else ctypes.c_void_p( offset )
    GL.glIndexPointer( glType, stride, offset )

def set_attribute_pointer(
    location,
    values_per_vertex,
    glType,
    stride,
    offset,
    normalise = False
    ):
    if offset == 0:
        offset = None
    else:
        offset = ctypes.c_void_p( offset )

    GL.glVertexAttribPointer(
        location,
        values_per_vertex,
        glType,
        GL.GL_TRUE if normalise else GL.GL_FALSE,
        stride,
        offset
        )


class Buffer( object ):
    """Wrapper around the glGenBuffers related functions.

    A Buffer is composed of an OpenGL buffer and a list of BufferRegions.
    Each BufferRegion defines the a contiguous region of the buffer
    and the format of data provided in that region.

    For example, a Buffer composed of 2 regions.
    [ Interleaved Vertex Data ][ Animation weights ]
    The first region is composed of interleaved vertex data, such as
    position, colour, normal.
    The second region is composed of animation data, such as weights and
    indices.

    This enables a single buffer to provide data for many attributes.

    Each BufferRegion has an associated Numpy dtype.
    The dtype is used to calculate data offsets which provide enough
    information to enable OpenGL to index into the data.
    """

    def __init__(
        self,
        target = GL.GL_ARRAY_BUFFER,
        usage = GL.GL_STATIC_DRAW,
        *args,
        **kwargs
        ):
        """Creates a Buffer object.

        The 'target' parameter matches that of the OpenGL 'target'
        parameter in the glBufferData and related functions.

        The 'usage' parameter matches that of the OpenGL 'usage'
        parameter in the glBufferData and related functions.

        The *args parameters is a list of regions.
        Each value is a tuple and consists of the following values:
            (count, dtype)
        Where count is the number of rows of data in the format specified
        by 'dtype'.
        And 'dtype' is a numpy dtype string or numpy.dtype object.

        A Buffer object cannot be resized once created.
        To change a Buffer's size, create a new Buffer object
        and pass the existing Buffer's handle in as the 'handle'
        parameter.
        """
        super( Buffer, self ).__init__()

        self._target = target
        self._usage = usage
        self._nbytes = 0

        handle = kwargs.get( 'handle', None )
        self._handle = GL.glGenBuffers( 1 ) if not handle else handle

        self._regions = []
        # iterate through our formats and create our region objects
        for (row_count, dtype) in args:
            region = BufferRegion( self, row_count, dtype, self._nbytes )

            self._regions.append( region )
            self._nbytes += region.nbytes

        # set the buffer size
        self.bind()
        GL.glBufferData( self.target, self.nbytes, None, self.usage )
        self.unbind()

    @property
    def target( self ):
        return self._target

    @property
    def handle( self ):
        return self._handle

    @property
    def nbytes( self ):
        return self._nbytes

    @property
    def usage( self ):
        return self._usage

    def __getitem__( self, index ):
        return self._regions[ index ]

    def __iter__( self ):
        return self.next()

    def next( self ):
        for region in self._regions:
            yield region

    def bind( self ):
        assert currently_bound_buffer( self._target ) != self._handle

        GL.glBindBuffer( self.target, self.handle )

    def unbind( self ):
        assert currently_bound_buffer( self._target ) == self._handle

        GL.glBindBuffer( self.target, 0 )

    @parameters_as_numpy_arrays( 'data' )
    def set_data( self, data ):
        assert currently_bound_buffer( self._target ) == self._handle

        GL.glBufferSubData( self.buffer.target, 0, data.nbytes, data )

    """
    # see following link for possible issue that needs testing
    # http://www.mail-archive.com/numpy-discussion@lists.sourceforge.net/msg01161.html
    def map( self, access = GL.GL_READ_WRITE ):
        return GL.glMapBuffer( self.target, access )

    def unmap( self ):
        GL.glUnmapBuffer( self.target )
    """

    def push_attributes( self ):
        """Pushes the enable and pointer state of vertex arrays.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glPushClientAttrib( GL.GL_CLIENT_VERTEX_ARRAY_BIT )

    def pop_attributes( self ):
        """Pops the enable and pointer state of vertex arrays.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glPopClientAttrib()

    def enable_vertex_pointer( self ):
        GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

    def disable_vertex_pointer( self ):
        GL.glDisableClientState( GL.GL_VERTEX_ARRAY )

    def set_vertex_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        """Sets the glVertexPointer.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

        set_vertex_pointer( values_per_vertex, glType, stride, offset )

    def enable_color_pointer( self ):
        GL.glEnableClientState( GL.GL_COLOR_ARRAY )

    def disable_color_pointer( self ):
        GL.glDisableClientState( GL.GL_COLOR_ARRAY )

    def set_color_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        """Sets the glColorPointer.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_COLOR_ARRAY )

        set_color_pointer( values_per_vertex, glType, stride, offset )

    def enable_texture_coord_pointer( self ):
        GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

    def disable_texture_coord_pointer( self ):
        GL.glDisableClientState( GL.GL_TEXTURE_COORD_ARRAY )

    def set_texture_coord_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        """Sets the glTexCoordPointer.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

        set_texture_coord_pointer( values_per_vertex, glType, stride, offset )

    def enable_normal_pointer( self ):
        GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

    def disable_normal_pointer( self ):
        GL.glDisableClientState( GL.GL_NORMAL_ARRAY )

    def set_normal_pointer( self, glType, stride, offset, enable = True ):
        """Sets the glNormalPointer.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

        set_normal_pointer( glType, stride, offset )

    def enable_index_pointer( self ):
        GL.glEnableClientState( GL.GL_INDEX_ARRAY )

    def disable_index_pointer( self ):
        GL.glDisableClientState( GL.GL_INDEX_ARRAY )

    def set_index_pointer( self, glType, stride, offset, enable = True ):
        """Sets the glIndexPointer.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_INDEX_ARRAY )

        set_index_pointer( glType, stride, offset )

    def enable_shader_attribute( self, shader, attribute ):
        location = shader.attributes[ attribute ]
        GL.glEnableVertexAttribArray( location )

    def disable_shader_attribute( self, shader, attribute ):
        location = shader.attributes[ attribute ]
        GL.glDisableVertexAttribArray( location )

    def enable_attribute( self, index ):
        GL.glEnableVertexAttribArray( index )

    def disable_attribute( self, index ):
        GL.glDisableVertexAttribArray( index )

    def set_attribute_pointer(
        self,
        location,
        values_per_vertex,
        glType,
        stride,
        offset,
        normalise = False,
        enable = True
        ):
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableVertexAttribArray( location )

        set_attribute_pointer(
            location,
            values_per_vertex,
            glType,
            stride,
            offset,
            normalise
            )

    def __str__( self ):
        string = \
            "BufferRegion:\n" \
            "nbytes:\t%s\n"  % (
                self.nbytes
                )
        for region in self._regions:
            string += str(region) + "\n"
        return string[:-1]


class BufferRegion( object ):
    """Wraps a region of the GL Buffer.

    Each region has an associated numpy dtype object.
    This enabled a region to provide enough information for
    OpenGL Vertex Array Objects.
    """

    def __init__( self, buffer, row_count, dtype, offset = 0 ):
        super( BufferRegion, self ).__init__()

        self._buffer = buffer
        self._rows = row_count
        self._dtype = dtype
        self._offset = offset

    @property
    def buffer( self ):
        return self._buffer

    @property
    def dtype( self ):
        return self._dtype

    @property
    def rows( self ):
        return self._rows

    @property
    def nbytes( self ):
        return self._rows * self._dtype.itemsize

    @property
    def stride( self ):
        """Returns the stride of the buffer
        """
        return self._dtype.itemsize

    def type( self, name = None ):
        return numpy_utils.dtype_gl_enum( self._dtype, name )

    def offset( self, name = None ):
        """Returns the initial offset of the named property
        """
        if name:
            return self._offset + numpy_utils.dtype_offset( self._dtype, name )
        else:
            return self._offset

    def element_count( self, name = None ):
        return numpy_utils.dtype_element_count( self._dtype, name )

    @parameters_as_numpy_arrays( 'data' )
    def set_data( self, data ):
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle

        GL.glBufferSubData( self.buffer.target, self._offset, data.nbytes, data )

    def push_attributes( self ):
        """Pushes the enable and pointer state of vertex arrays.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glPushClientAttrib( GL.GL_CLIENT_VERTEX_ARRAY_BIT )

    def pop_attributes( self ):
        """Pops the enable and pointer state of vertex arrays.
        
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glPopClientAttrib()

    def enable_vertex_pointer( self ):
        GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

    def disable_vertex_pointer( self ):
        GL.glDisableClientState( GL.GL_VERTEX_ARRAY )

    def set_vertex_pointer( self, name = None, enable = True ):
        """Calculates and sets the glVertexPointer to the specified
        dtype attribute.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle

        values_per_vertex = self.element_count( name )
        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        if enable:
            GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

        set_vertex_pointer( values_per_vertex, glType, stride, offset )

    def enable_color_pointer( self ):
        GL.glEnableClientState( GL.GL_COLOR_ARRAY )

    def disable_color_pointer( self ):
        GL.glDisableClientState( GL.GL_COLOR_ARRAY )

    def set_color_pointer( self, name = None, enable = True ):
        """Calculates and sets the glColorPointer to the specified
        dtype attribute.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle

        values_per_vertex = self.element_count( name )
        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        if enable:
            GL.glEnableClientState( GL.GL_COLOR_ARRAY )

        set_color_pointer( values_per_vertex, glType, stride, offset )

    def enable_texture_coord_pointer( self ):
        GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

    def disable_texture_coord_pointer( self ):
        GL.glDisableClientState( GL.GL_TEXTURE_COORD_ARRAY )

    def set_texture_coord_pointer( self, name = None, enable = True ):
        """Calculates and sets the glTexCoordPointer to the specified
        dtype attribute.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle

        values_per_vertex = self.element_count( name )
        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        if enable:
            GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

        set_texture_coord_pointer( values_per_vertex, glType, stride, offset )

    def enable_normal_pointer( self ):
        GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

    def disable_normal_pointer( self ):
        GL.glDisableClientState( GL.GL_NORMAL_ARRAY )

    def set_normal_pointer( self, name = None, enable = True ):
        """Calculates and sets the glNormalPointer to the specified
        dtype attribute.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle

        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        if enable:
            GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

        set_normal_pointer( glType, stride, offset )

    def enable_index_pointer( self ):
        GL.glEnableClientState( GL.GL_INDEX_ARRAY )

    def disable_index_pointer( self ):
        GL.glDisableClientState( GL.GL_INDEX_ARRAY )

    def set_index_pointer( self, name = None, enable = True ):
        """Calculates and sets the glIndexPointer to the specified
        dtype attribute.

        This is an OpenGL Legacy function (<=2.1) and should not be
        called for Core profile applications (>=3.0).
        """
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle

        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        if enable:
            GL.glEnableClientState( GL.GL_INDEX_ARRAY )

        set_index_pointer( glType, stride, offset )

    def enable_shader_attribute( self, shader, attribute ):
        location = shader.attributes[ attribute ]
        GL.glEnableVertexAttribArray( location )

    def disable_shader_attribute( self, shader, attribute ):
        location = shader.attributes[ attribute ]
        GL.glDisableVertexAttribArray( location )

    def enable_attribute( self, index ):
        GL.glEnableVertexAttribArray( index )

    def disable_attribute( self, index ):
        GL.glDisableVertexAttribArray( index )

    def set_attribute_pointer(
        self,
        shader,
        attribute,
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
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle

        # get the attribute location
        location = shader.attributes[ attribute ].location

        values_per_vertex = self.element_count( name )
        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        if enable:
            GL.glEnableVertexAttribArray( location )

        set_attribute_pointer(
            location,
            values_per_vertex,
            glType,
            stride,
            offset,
            normalise
            )

    def __str__( self ):
        string = \
            "BufferRegion:\n" \
            "dtype:\t%s\n" \
            "rows:\t%d\n" \
            "nbytes:\t%d\n" \
            "stride:\t%d\n" \
            "offset:\t%d"  % (
                str(self._dtype),
                self._rows,
                self.nbytes,
                self.stride,
                self._offset,
                )
        return string

