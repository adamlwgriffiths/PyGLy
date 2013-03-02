"""
TODO: get gl buffer limit values
"""

import ctypes

from OpenGL import GL

from pyrr.utils import \
    all_parameters_as_numpy_arrays, \
    parameters_as_numpy_arrays

from pygly import \
    numpy_utils, \
    gl_utils

class Buffer( object ):

    def __init__( self, target = GL.GL_ARRAY_BUFFER, usage = GL.GL_STATIC_DRAW ):
        super( Buffer, self ).__init__()

        self._target = target
        self._handle = GL.glGenBuffers( 1 )
        self._nbytes = 0
        self._usage = usage

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

    def bind( self ):
        GL.glBindBuffer( self.target, self.handle )

    def unbind( self ):
        GL.glBindBuffer( self.target, 0 )

    def reset( self, nbytes, usage = GL.GL_STATIC_DRAW ):
        self._usage = usage
        self._nbytes = nbytes
        GL.glBufferData( self.target, self.nbytes, None, self.usage )

    @parameters_as_numpy_arrays( 'data' )
    def set_data( self, data, usage = None ):
        if usage:
            self._usage = usage
        self._nbytes = data.nbytes
        GL.glBufferData( self.target, self.nbytes, data, self.usage )

    @parameters_as_numpy_arrays( 'data' )
    def set_sub_data( self, data, offset = 0 ):
        GL.glBufferSubData( self.target, offset, data.nbytes, data )

    """
    # see following link for possible issue that needs testing
    # http://www.mail-archive.com/numpy-discussion@lists.sourceforge.net/msg01161.html
    def map( self, access = GL.GL_READ_WRITE ):
        if access not in valid_access:
            raise ValueError( "Not a valid buffer access type" )

        return GL.glMapBuffer( self.target, access )

    def unmap( self ):
        GL.glUnmapBuffer( self.target )
    """

    def vertex_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

        GL.glVertexPointer( values_per_vertex, glType, stride, offset )

    def color_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_COLOR_ARRAY )

        GL.glColorPointer( values_per_vertex, glType, stride, offset )

    def texture_coord_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

        glTexCoordPointer( values_per_vertex, glType, stride, offset )

    def normal_pointer( self, glType, stride, offset, enable = True ):
        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

        GL.glNormalPointer( glType, stride, offset )

    def index_pointer( self, glType, stride, offset, enable = True ):
        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_INDEX_ARRAY )

        GL.glIndexPointer( glType, stride, offset )

    def __str__( self ):
        string = \
            "BufferRegion:\n" \
            "nbytes:\t%s" % (
                self.nbytes,
                )
        return string

class TypedBuffer( object ):
    """Simple wrapper around the glGenBuffers related functions.

    A TypedBuffer is composed of an OpenGL buffer and a list of BufferRegions.
    Each BufferRegion defines the format of data provided in that region of
    the bufferion.

    For example, a TypedBuffer composed of 2 regions.
    [ Interleaved Vertex Data ][ Animation weights ]
    The first region is composed of interleaved vertex data, such as
    position, colour, normal.
    The second region is composed of animation data, such as weights and
    indices.

    This enables a single buffer to provide data for many attributes.

    BufferRegions provide enough information to allow OpenGL to index into
    the Buffer.
    """


    def __init__( self, target = GL.GL_ARRAY_BUFFER, usage = GL.GL_STATIC_DRAW, *args ):
        super( TypedBuffer, self ).__init__()

        self._target = target
        self._usage = usage
        self._handle = GL.glGenBuffers( 1 )
        self._nbytes = 0

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
        GL.glBindBuffer( self.target, self.handle )

    def unbind( self ):
        GL.glBindBuffer( self.target, 0 )

    @parameters_as_numpy_arrays( 'data' )
    def set_data( self, data ):
        GL.glBufferSubData( self.buffer.target, 0, data.nbytes, data )

    """
    # see following link for possible issue that needs testing
    # http://www.mail-archive.com/numpy-discussion@lists.sourceforge.net/msg01161.html
    def map( self, access = GL.GL_READ_WRITE ):
        return GL.glMapBuffer( self.target, access )

    def unmap( self ):
        GL.glUnmapBuffer( self.target )
    """

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
        return self.rows * self._dtype.itemsize

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
        GL.glBufferSubData( self.buffer.target, self._offset, data.nbytes, data )

    def get_data( self ):
        pass

    def vertex_pointer( self, name = None, enable = True ):
        values_per_vertex = self.element_count( name )
        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

        GL.glVertexPointer( values_per_vertex, glType, stride, offset )

    def color_pointer( self, name = None, enable = True ):
        values_per_vertex = self.element_count( name )
        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_COLOR_ARRAY )

        GL.glColorPointer( values_per_vertex, glType, stride, offset )

    def texture_coord_pointer( self, name = None, enable = True ):
        values_per_vertex = self.element_count( name )
        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

        glTexCoordPointer( values_per_vertex, glType, stride, offset )

    def normal_pointer( self, name = None, enable = True ):
        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

        GL.glNormalPointer( glType, stride, offset )

    def index_pointer( self, name = None, enable = True ):
        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        offset = None if offset == 0 else ctypes.c_void_p( offset )

        if enable:
            GL.glEnableClientState( GL.GL_INDEX_ARRAY )

        GL.glIndexPointer( glType, stride, offset )

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

