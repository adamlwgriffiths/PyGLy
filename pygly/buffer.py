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

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    offset = None if offset == 0 else ctypes.c_void_p( offset )
    GL.glVertexPointer( values_per_vertex, glType, stride, offset )

def set_color_pointer( values_per_vertex, glType, stride, offset ):
    """Sets the glColorPointer.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    offset = None if offset == 0 else ctypes.c_void_p( offset )
    GL.glColorPointer( values_per_vertex, glType, stride, offset )

def set_texture_coord_pointer( values_per_vertex, glType, stride, offset ):
    """Sets the glTexCoordPointer.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    offset = None if offset == 0 else ctypes.c_void_p( offset )
    GL.glTexCoordPointer( values_per_vertex, glType, stride, offset )

def set_normal_pointer( glType, stride, offset ):
    """Sets the glNormalPointer.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    offset = None if offset == 0 else ctypes.c_void_p( offset )
    GL.glNormalPointer( glType, stride, offset )

def set_index_pointer( glType, stride, offset ):
    """Sets the glIndexPointer.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
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
    """Sets the attribute pointer.

    This is the equivalent of calling glVertexAttribPointer.
    Handles quirks in PyOpenGL that require specific values
    in certain cases.
    """
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

    .. seealso:
        Class :py:class:`pygly.buffer.BufferRegion`
    """

    def __init__(
        self,
        target = GL.GL_ARRAY_BUFFER,
        usage = GL.GL_STATIC_DRAW,
        *args,
        **kwargs
        ):
        """Creates a Buffer object.

        A buffer's size is fixed once created.

        A buffer is copied of regions. Each region defines the data format
        and size of its data.

        :param target: Matches that of the OpenGL 'target'
        parameter in the glBufferData and related functions.

        :param usage: Matches that of the OpenGL 'usage'
            parameter in the glBufferData and related functions.

        :param *args: A list of regions.
            Each value is a tuple and consists of the following values:
                (count, dtype)
            Where count is the number of rows of data in the format specified
            by 'dtype'.
            And 'dtype' is a numpy dtype string or numpy.dtype object.

        :param handle: An existing Buffer's handle.
            This can be used to resize a buffer by taking the handle from
            one buffer object and passing it to a new, resized, buffer.
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
        """The OpenGL target type of the buffer.

        :rtype: int
        :return: The target type of the buffer.
            For most purposes, this will be GL_ARRAY_BUFFER.
        """
        return self._target

    @property
    def handle( self ):
        """The OpenGL handle for this buffer.
        """
        return self._handle

    @property
    def nbytes( self ):
        """The size of this buffer in bytes.
        """
        return self._nbytes

    @property
    def usage( self ):
        """The OpenGL usage flag of this buffer.
        """
        return self._usage

    def __getitem__( self, index ):
        """Returns the region object at the specified index.

        :rtype: BufferRegion
        :return: The specified buffer region.
        :raise IndexError: Raised if the index is invalid.
        """
        return self._regions[ index ]

    def __iter__( self ):
        """Provides iterator into the Buffer returning BufferRegions.

        :rtype: BufferRegion.
        """
        return self.next()

    def next( self ):
        """Provides iterator into the Buffer returning BufferRegions.

        :rtype: BufferRegion.
        """
        for region in self._regions:
            yield region

    def bind( self ):
        """Binds the current buffer.

        This will make the buffer the currently active buffer.

        Asserts that the buffer is not currently bound.
        """
        assert currently_bound_buffer( self._target ) != self._handle

        GL.glBindBuffer( self.target, self.handle )

    def unbind( self ):
        """Unbinds the current buffer.

        This will deactivate the buffer.

        Asserts that the buffer is currently bound.
        """
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
        """Enables the vertex data for rendering.

        If vertex data is not enabled before rendering, the data
        will be ignored by OpenGL.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

    def disable_vertex_pointer( self ):
        """Disables the vertex data.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_VERTEX_ARRAY )

    def set_vertex_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        """Sets the glVertexPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

        set_vertex_pointer( values_per_vertex, glType, stride, offset )

    def enable_color_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_COLOR_ARRAY )

    def disable_color_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_COLOR_ARRAY )

    def set_color_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        """Sets the glColorPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_COLOR_ARRAY )

        set_color_pointer( values_per_vertex, glType, stride, offset )

    def enable_texture_coord_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

    def disable_texture_coord_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_TEXTURE_COORD_ARRAY )

    def set_texture_coord_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        """Sets the glTexCoordPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

        set_texture_coord_pointer( values_per_vertex, glType, stride, offset )

    def enable_normal_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

    def disable_normal_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_NORMAL_ARRAY )

    def set_normal_pointer( self, glType, stride, offset, enable = True ):
        """Sets the glNormalPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

        set_normal_pointer( glType, stride, offset )

    def enable_index_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_INDEX_ARRAY )

    def disable_index_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_INDEX_ARRAY )

    def set_index_pointer( self, glType, stride, offset, enable = True ):
        """Sets the glIndexPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        assert currently_bound_buffer( self._target ) == self._handle

        if enable:
            GL.glEnableClientState( GL.GL_INDEX_ARRAY )

        set_index_pointer( glType, stride, offset )

    def enable_shader_attribute( self, shader, attribute ):
        """Enables the attribute at the index that matches the location of
        the specified shader attribute.

        :param Shader shader: The shader object.
        :param string attribute: The attribute name to enable.
        """
        location = shader.attributes[ attribute ]
        GL.glEnableVertexAttribArray( location )

    def disable_shader_attribute( self, shader, attribute ):
        """Disables the attribute at the index that matches the location of
        the specified shader attribute.

        :param Shader shader: The shader object.
        :param string attribute: The attribute name to disable.
        """
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

    .. seealso:
        Class :py:class:`pygly.buffer.Buffer`
    """

    def __init__( self, buffer, row_count, dtype, offset = 0 ):
        super( BufferRegion, self ).__init__()

        self._buffer = buffer
        self._rows = row_count
        self._dtype = dtype
        self._offset = offset

    @property
    def buffer( self ):
        """The Buffer this BufferRegion belongs to.

        :rtype: Buffer
        """
        return self._buffer

    @property
    def dtype( self ):
        """The numpy.dtype that defines this region.

        :rtype: numpy.dtype
        """
        return self._dtype

    @property
    def rows( self ):
        """The number of rows of data this region contains.

        A row is a single block of values that match the specified dtype.
        A row of data is of size 'stride' bytes.

        :rtype: int
        """
        return self._rows

    @property
    def nbytes( self ):
        """The number of bytes in this region.

        Where::
            nbytes = stride * rows

        :rtype: int
        """
        return self._rows * self._dtype.itemsize

    @property
    def stride( self ):
        """Returns the stride of the buffer.

        The stride is the size of a single block of the specified dtype.
        """
        return self._dtype.itemsize

    def type( self, name = None ):
        """The OpenGL enumeration type for the specified named property.

        The name must match a name within the region's dtype.

        If a name is not given, the buffer will attempt to perform the conversion
        with the assumption that the dtype contains a single data type.

        :rtype: int
        :return: The OpenGL enumeration value representing the data type.
            Valid values are::
                GL_BYTE,
                GL_UNSIGNED_BYTE,
                GL_SHORT,
                GL_UNSIGNED_SHORT,
                GL_INT,
                GL_UNSIGNED_INT,
                GL_FLOAT,
                GL_DOUBLE,

        .. seealso: `py:func:pygly.numpy_utils.dtype_gl_enum`
        """
        return numpy_utils.dtype_gl_enum( self._dtype, name )

    def offset( self, name = None ):
        """The byte offset for data of the named property.

        The name must match a name within the region's dtype.

        If a name is not given the result will be 0.

        :rtype: int
        :return: The offset of the data in bytes.
        :raise KeyError: Raised if the specified name does not exist.
        """
        if name:
            return self._offset + numpy_utils.dtype_offset( self._dtype, name )
        else:
            return self._offset

    def element_count( self, name = None ):
        """The number of values for the specified named property in each row.

        If a name is not given, the buffer will attempt to perform the calculation
        with the assumption that the dtype contains a single data type.
        If this is not true, a ValueError exception will be raised.

        :rtype: int
        :return: The number of values in the specified named property.
        :raise ValueError: Raised if the specified name does not exist, or if
            no name was provided but there is more than one named property in the
            dtype.
        """
        return numpy_utils.dtype_element_count( self._dtype, name )

    @parameters_as_numpy_arrays( 'data' )
    def set_data( self, data ):
        """Sets the regions data.

        Data will be set from the start of the region.

        :raise ValueError: Raised if the data size exceeds the region's bounds.
        """
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle
        if data.nbytes > self.nbytes:
            raise ValueError( "Data exceeds region bounds" )

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
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

    def disable_vertex_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_VERTEX_ARRAY )

    def set_vertex_pointer( self, name = None, enable = True ):
        """Calculates and sets the glVertexPointer to the specified
        dtype attribute.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
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
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_COLOR_ARRAY )

    def disable_color_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_COLOR_ARRAY )

    def set_color_pointer( self, name = None, enable = True ):
        """Calculates and sets the glColorPointer to the specified
        dtype attribute.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
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
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

    def disable_texture_coord_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_TEXTURE_COORD_ARRAY )

    def set_texture_coord_pointer( self, name = None, enable = True ):
        """Calculates and sets the glTexCoordPointer to the specified
        dtype attribute.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
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
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

    def disable_normal_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_NORMAL_ARRAY )

    def set_normal_pointer( self, name = None, enable = True ):
        """Calculates and sets the glNormalPointer to the specified
        dtype attribute.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle

        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        if enable:
            GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

        set_normal_pointer( glType, stride, offset )

    def enable_index_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_INDEX_ARRAY )

    def disable_index_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_INDEX_ARRAY )

    def set_index_pointer( self, name = None, enable = True ):
        """Calculates and sets the glIndexPointer to the specified
        dtype attribute.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        assert currently_bound_buffer( self.buffer.target ) == self.buffer.handle

        glType = self.type( name )
        stride = self.stride
        offset = self.offset( name )

        if enable:
            GL.glEnableClientState( GL.GL_INDEX_ARRAY )

        set_index_pointer( glType, stride, offset )

    def enable_shader_attribute( self, shader, attribute ):
        """Enables the attribute at the index that matches the location of
        the specified shader attribute.

        This is the same as Buffer.enable_shader_attribute.

        .. seealso:
            :py:func:`pygly.buffer.Buffer.enable_shader_attribute`

        :param Shader shader: The shader object.
        :param string attribute: The attribute name to enable.
        """
        location = shader.attributes[ attribute ]
        GL.glEnableVertexAttribArray( location )

    def disable_shader_attribute( self, shader, attribute ):
        """Disables the attribute at the index that matches the location of
        the specified shader attribute.

        This is the same as Buffer.disable_shader_attribute.

        .. seealso:
            `py:func:pygly.buffer.Buffer.disable_shader_attribute`

        :param Shader shader: The shader object.
        :param string attribute: The attribute name to disable.
        """
        location = shader.attributes[ attribute ]
        GL.glDisableVertexAttribArray( location )

    def enable_attribute( self, index ):
        """Enables the attribute at the specified index.
        """
        GL.glEnableVertexAttribArray( index )

    def disable_attribute( self, index ):
        """Disables the attribute at the specified index.
        """
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

        :param Shader shader: The shader object.
        :param string attribute: The name of a shader attribute variable.
        :param string name: A named property defined by this region's dtype.

        For example::
            import textwrap
            import numpy
            from OpenGL import GL
            from pygly.shader import Shader, ShaderProgram
            from pygly.buffer import Buffer, BufferRegion

            vertex_shader = textwrap.dedent( '''
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
                ''' )

            fragment_shader = textwrap.dedent( '''
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
                ''' )

            # create our shader
            shader = ShaderProgram(
                Shader( GL.GL_VERTEX_SHADER, vertex_shader ),
                Shader( GL.GL_FRAGMENT_SHADER, fragment_shader )
                )

            vertices = numpy.array(
                [
                    #  X    Y    Z          R    G    B
                    (( 0.0, 1.0, 0.0),     (1.0, 0.0, 0.0)),
                    ((-2.0,-1.0, 0.0),     (0.0, 1.0, 0.0)),
                    (( 2.0,-1.0, 0.0),     (0.0, 0.0, 1.0)),
                    ],
                dtype = [
                    ('position',    'float32',  (3,)),
                    ('colour',      'float32',  (3,)),
                    ]
                )
            buffer = Buffer(
                GL.GL_ARRAY_BUFFER,
                GL.GL_STATIC_DRAW,
                (vertices.size, vertices.dtype)
                )
            buffer.bind()
            buffer[ 0 ].set_data( vertices )
            buffer[ 0 ].set_attribute_pointer( self.shader, 'in_position', 'position' )
            buffer.unbind()
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

