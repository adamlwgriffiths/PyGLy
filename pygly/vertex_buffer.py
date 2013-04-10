import ctypes

from OpenGL import GL

from pyrr.utils import parameters_as_numpy_arrays


def currently_bound_buffer( type ):
    """Returns the handle of the currently bound buffer.

    The buffer target type is required as there are 3 different
    buffer properties we can check.

    OpenGL provides individual binding stacks for the following
    buffer target types stacks:
        * GL_TEXTURE_BUFFER
        * GL_ELEMENT_ARRAY_BUFFER
        * All other buffer target types.

    :param int type: The buffer target type.
    :rtype: int
    :return: The handle of the currently bound buffer.
    """
    if type == GL.GL_TEXTURE_BUFFER:
        enum = GL.GL_TEXTURE_BUFFER_BINDING
    elif type == GL.GL_ELEMENT_ARRAY_BUFFER:
        enum = GL.GL_ELEMENT_ARRAY_BUFFER_BINDING
    else:
        enum = GL.GL_ARRAY_BUFFER_BINDING

    return GL.glGetInteger( enum )

def push_attributes():
    """Pushes the enable and pointer state of vertex arrays.

    This is used to store the state of the vertex attributes in OpenGL
    which can then be popped later to return the stack to a previous state.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glPushClientAttrib( GL.GL_CLIENT_VERTEX_ARRAY_BIT )

def pop_attributes():
    """Pops the enable and pointer state of vertex arrays.

    Returns the vertex attribute state to the state it was in when
    push_attributes was called.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glPopClientAttrib()

def enable_vertex_pointer():
    """Enables the vertex position data for rendering.

    If vertex data is not enabled before rendering, the data
    will be ignored by OpenGL.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

def disable_vertex_pointer():
    """Disables the vertex position data.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glDisableClientState( GL.GL_VERTEX_ARRAY )

def set_vertex_pointer( values_per_vertex, glType, stride, offset):
    """Sets the glVertexPointer.

    .. note:: This function automatically handles a quirk in PyOpenGL
    where an offset of 0 must be specified as None.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    offset = ctypes.c_void_p( offset ) if offset else None
    GL.glVertexPointer( values_per_vertex, glType, stride, offset )

def enable_color_pointer():
    """Enables the vertex colour data for rendering.

    If vertex colour data is not enabled before rendering, the colour
    data will be ignored by OpenGL.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glEnableClientState( GL.GL_COLOR_ARRAY )

def disable_color_pointer():
    """Disables the vertex colour data.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glDisableClientState( GL.GL_COLOR_ARRAY )

def set_color_pointer( values_per_vertex, glType, stride, offset ):
    """Sets the glColorPointer.

    .. note:: This function automatically handles a quirk in PyOpenGL
    where an offset of 0 must be specified as None.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    offset = ctypes.c_void_p( offset ) if offset else None
    GL.glColorPointer( values_per_vertex, glType, stride, offset )

def enable_texture_coord_pointer():
    """Enables the vertex texture co-ordinate data for rendering.

    If vertex texture co-ordinate data is not enabled before rendering,
    the texture co-ordinate data will be ignored by OpenGL.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

def disable_texture_coord_pointer():
    """Disables the vertex texture co-ordinate data.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glDisableClientState( GL.GL_TEXTURE_COORD_ARRAY )

def set_texture_coord_pointer( values_per_vertex, glType, stride, offset ):
    """Sets the glTexCoordPointer.

    .. note:: This function automatically handles a quirk in PyOpenGL
    where an offset of 0 must be specified as None.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    offset = ctypes.c_void_p( offset ) if offset else None
    GL.glTexCoordPointer( values_per_vertex, glType, stride, offset )

def enable_normal_pointer():
    """Enables the vertex normal data for rendering.

    If vertex normal data is not enabled before rendering, the normal
    data will be ignored by OpenGL.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

def disable_normal_pointer():
    """Disables the vertex normal data.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glDisableClientState( GL.GL_NORMAL_ARRAY )

def set_normal_pointer( glType, stride, offset ):
    """Sets the glNormalPointer.

    .. note:: This function automatically handles a quirk in PyOpenGL
    where an offset of 0 must be specified as None.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    offset = ctypes.c_void_p( offset ) if offset else None
    GL.glNormalPointer( glType, stride, offset )

def enable_index_pointer():
    """Enables the vertex index data for rendering.

    If vertex index data is not enabled before rendering, the index
    data will be ignored by OpenGL and the vertices will be rendered
    as an ordered list.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glEnableClientState( GL.GL_INDEX_ARRAY )

def disable_index_pointer():
    """Disables the vertex index data.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glDisableClientState( GL.GL_INDEX_ARRAY )

def set_index_pointer( glType, stride, offset ):
    """Sets the glIndexPointer.

    This function automatically handles a quirk in PyOpenGL
    where an offset of 0 must be specified as None.

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    offset = ctypes.c_void_p( offset ) if offset else None
    GL.glIndexPointer( glType, stride, offset )

def enable_shader_attribute( shader, attribute ):
    """Enables the attribute at the index that matches the location of
    the specified shader attribute.

    If vertex attribute data is not enabled before rendering, the attribute
    data will be ignored by OpenGL.

    :param pygly.shader.ShaderProgram shader: The shader object.
    :param string attribute: The attribute name to enable.
    """
    location = shader.attributes[ attribute ].location
    GL.glEnableVertexAttribArray( location )

def disable_shader_attribute( shader, attribute ):
    """Disables the attribute at the index that matches the location of
    the specified shader attribute.

    :param pygly.shader.ShaderProgram shader: The shader object.
    :param string attribute: The attribute name to disable.
    """
    location = shader.attributes[ attribute ].location
    GL.glDisableVertexAttribArray( location )

def enable_attribute_pointer( index ):
    """Enables the attribute at the specified index.

    If vertex attribute data is not enabled before rendering, the attribute
    data will be ignored by OpenGL.

    :param int index: The index to enable.
    """
    GL.glEnableVertexAttribArray( index )

def disable_attribute_pointer( index ):
    """Disables the attribute at the specified index.

    :param int index: The index to disable.
    """
    GL.glDisableVertexAttribArray( index )

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

    This function automatically handles a quirk in PyOpenGL
    where an offset of 0 must be specified as None.
    """
    normalise = GL.GL_TRUE if normalise else GL.GL_FALSE
    offset = ctypes.c_void_p( offset ) if offset else None

    GL.glVertexAttribPointer(
        location,
        values_per_vertex,
        glType,
        normalise,
        stride,
        offset
        )


class VertexBuffer( object ):


    @parameters_as_numpy_arrays( 'data' )
    def __init__(
        self,
        target = GL.GL_ARRAY_BUFFER,
        usage = GL.GL_STATIC_DRAW,
        nbytes = None,
        data = None,
        handle = None
        ):
        """Creates a Vertex Buffer with the specified attributes.

        The usage parameter can be changed by calling allocate with
        a different usage.

        :param int nbytes: If passed in, the buffer will be allocated.
        :param numpy.array data: If passed in, it will over-ride nbytes and will also
            populate the buffer with the specified data.
        :param int handle: If passed in, the buffer will use the specified handle
            instead of creating a new one.
            If the target differs from the original buffer, an error will
            be triggered by OpenGL when the buffer is used.
        """
        super( VertexBuffer, self ).__init__()

        self._target = target
        self._usage = usage
        self._nbytes = 0

        self.handle = GL.glGenBuffers( 1 ) if not handle else handle

        if data != None:
            nbytes = data.nbytes

        if nbytes:
            self.bind()
            self.allocate( usage, nbytes )
            if data != None:
                self.set_data( data )
            self.unbind()

    @property
    def target( self ):
        return self._target

    @property
    def usage( self ):
        return self._usage

    @property
    def nbytes( self ):
        return self._nbytes

    @property
    def bound( self ):
        """Returns the bind state of the buffer.

        :rtype: boolean
        :return: Returns True if the buffer is currently bound.
        """
        return currently_bound_buffer( self.target ) == self.handle

    def bind( self ):
        """Unbinds the current buffer.

        This will deactivate the buffer.

        Asserts that the buffer is currently bound.
        """
        if self.bound:
            raise ValueError( "Buffer is already bound" )
        GL.glBindBuffer( self.target, self.handle )

    def unbind( self ):
        if not self.bound:
            raise ValueError( "Buffer is not bound" )
        GL.glBindBuffer( self.target, 0 )

    def allocate( self, usage, nbytes ):
        """Allocates a new buffer on the GPU.

        If the buffer has already been allocated, it will be freed.

        The handle is not changed by this operation.

        .. note:: Existing data will be lost.
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        GL.glBufferData( self.target, nbytes, None, usage )
        self._nbytes = nbytes
        self._usage = usage

    @parameters_as_numpy_arrays( 'data' )
    def set_data( self, data, offset = 0 ):
        """Populates the buffer with the specified data.

        The buffer must be allocated before data can be set.

        :raise ValueError: Raised if the buffer is not currently bound.
        :raise OverflowError: Raised if the data size exceeds the buffer's bounds.

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.allocate`
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        if (offset + data.nbytes) > self.nbytes:
            raise OverflowError( "Data would overflow buffer" )

        GL.glBufferSubData( self.target, offset, data.nbytes, data )

    def push_attributes( self ):
        """Pushes the enable and pointer state of vertex arrays.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        push_attributes()

    def pop_attributes( self ):
        """Pops the enable and pointer state of vertex arrays.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        pop_attributes()

    def enable_vertex_pointer( self ):
        """Enables the vertex data for rendering.

        If vertex data is not enabled before rendering, the data
        will be ignored by OpenGL.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        enable_vertex_pointer()

    def disable_vertex_pointer( self ):
        """Disables the vertex data.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        disable_vertex_pointer()

    def set_vertex_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        """Sets the glVertexPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_vertex_pointer`
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable_vertex_pointer()

        set_vertex_pointer( values_per_vertex, glType, stride, offset )

    def enable_color_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        enable_color_pointer()

    def disable_color_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        disable_color_pointer()

    def set_color_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        """Sets the glColorPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_color_pointer`
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable_color_pointer()

        set_color_pointer( values_per_vertex, glType, stride, offset )

    def enable_texture_coord_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        enable_texture_coord_pointer()

    def disable_texture_coord_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        disable_texture_coord_pointer()

    def set_texture_coord_pointer( self, values_per_vertex, glType, stride, offset, enable = True ):
        """Sets the glTexCoordPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_texture_coord_pointer`
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable_texture_coord_pointer()

        set_texture_coord_pointer( values_per_vertex, glType, stride, offset )

    def enable_normal_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        enable_normal_pointer()

    def disable_normal_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        disable_normal_pointer()

    def set_normal_pointer( self, glType, stride, offset, enable = True ):
        """Sets the glNormalPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_normal_pointer`
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable_normal_pointer()

        set_normal_pointer( glType, stride, offset )

    def enable_index_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        enable_index_pointer()

    def disable_index_pointer( self ):
        """
        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        disable_index_pointer()

    def set_index_pointer( self, glType, stride, offset, enable = True ):
        """Sets the glIndexPointer.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_index_pointer`
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable_index_pointer()

        set_index_pointer( glType, stride, offset )

    def enable_shader_attribute_pointer( self, shader, attribute ):
        """Enables the attribute at the index that matches the location of
        the specified shader attribute.

        :param Shader shader: The shader object.
        :param string attribute: The attribute name to enable.

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_attribute_pointer`
        """
        enable_shader_attribute( shader, attribute )

    def disable_shader_attribute_pointer( self, shader, attribute ):
        """Disables the attribute at the index that matches the location of
        the specified shader attribute.

        :param Shader shader: The shader object.
        :param string attribute: The attribute name to disable.

        """
        disable_shader_attribute( shader, attribute )

    def enable_attribute_pointer( self, index ):
        """Enables the attribute at the specified index.

        :param int index: The index to enable.

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.disable_shader_attribute_pointer`
        """
        enable_attribute_pointer( index )

    def disable_attribute_pointer( self, index ):
        """Disables the attribute at the specified index.

        :param int index: The index to disable.
        """
        disable_attribute_pointer( index )

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
        """Sets the glVertexAttribPointer.

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_attribute_pointer`
        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_shader_attribute_pointer`
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable_attribute_pointer( location )

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
            "%s:\n" \
            "nbytes:\t%s"  % (
                self.__class__.__name__,
                self.nbytes
                )
        return string
