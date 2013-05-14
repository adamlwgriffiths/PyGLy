import ctypes
from numbers import Number

import numpy
from OpenGL import GL

from pyrr.utils import parameters_as_numpy_arrays
from shader import Attribute as ShaderAttribute
import numpy_utils


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


    class Attribute( object ):

        def __init__( self, buffer ):
            super( VertexBuffer.Attribute, self ).__init__()

            self.buffer = buffer

        @property
        def float32( self ):
            # return an attribute class with GL_TYPE = GL_FLOAT
            # and a data size of 4 bytes
            # can use this information to determine the number of
            # values per vertex
            pass

        @property
        def float64( self ):
            pass

        @property
        def int32( self ):
            pass

        @property
        def int16( self ):
            pass

        @property
        def int8( self ):
            pass

        @property
        def uint32( self ):
            pass

        @property
        def uint16( self ):
            pass

        @property
        def uint8( self ):
            pass

        def __setitem__( self, index, data ):
            if not self.buffer.bound:
                raise ValueError( "Buffer is not bound" )

            # check the data type
            # we can only receive an integer or an attribute
            if isinstance( data, int ):
                location = data
            elif isinstance( data, ShaderAttribute ):
                location = data.location
            else:
                raise TypeError( "Cannot set attribute, data is of an unknown type" )

            # check the slice type
            if isinstance( index, slice ):
                # single slice
                pass
            elif isinstance( index, tuple ):
                # tuple of slices
                pass
            if isinstance( index, str ):
                stride = self.buffer.dtype.itemsize
                offset = numpy_utils.dtype_offset( self.buffer.dtype, index )
                values_per_vertex = numpy_utils.dtype_element_count( self.buffer.dtype, index )
                glType = numpy_utils.dtype_gl_enum( self.buffer.dtype, index )

                print location, values_per_vertex, glType, stride, offset

                # enable the attribute
                GL.glEnableVertexAttribArray( location )

                # set the pointer
                set_attribute_pointer(
                    location,
                    values_per_vertex,
                    glType,
                    stride,
                    offset
                    )
            else:
                # primitive
                pass

    @staticmethod
    def bound_buffer( type ):
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

    @classmethod
    def empty(
        cls,
        shape,
        target = GL.GL_ARRAY_BUFFER,
        usage = GL.GL_STATIC_DRAW,
        dtype = None,
        use_shadow_buffer = False,
        handle = None
        ):
        # just make the empty buffer
        buffer = cls(
            target,
            usage,
            dtype,
            shape,
            use_shadow_buffer,
            handle
            )
        # initialise the buffer's size
        buffer.bind()
        GL.glBufferData( buffer.target, buffer.nbytes, None, buffer.usage )
        buffer.unbind()

    @classmethod
    def zeros(
        cls,
        shape,
        target = GL.GL_ARRAY_BUFFER,
        usage = GL.GL_STATIC_DRAW,
        dtype = None,
        use_shadow_buffer = False,
        handle = None
        ):
        buffer = cls.array(
            target,
            usage,
            dtype,
            use_shadow_buffer,
            handle
            )
        # initialise the buffer's size
        object = numpy.zeros( shape, dtype = dtype )
        buffer.bind()
        GL.glBufferData( buffer.target, buffer.nbytes, None, buffer.usage )
        buffer[:] = object
        buffer.unbind()
        return buffer

    @classmethod
    def buffer(
        cls,
        object,
        target = GL.GL_ARRAY_BUFFER,
        usage = GL.GL_STATIC_DRAW,
        dtype = None,
        use_shadow_buffer = False,
        handle = None
        ):
        # handle other vertex buffers
        if isinstance( object, VertexBuffer ):
            # TODO
            raise TypeError( "Not currently supported" )

        # ensure we're working with a numpy array
        np_object = numpy.array( object )

        buffer = cls(
            target,
            usage,
            dtype if dtype else np_object.dtype,
            np_object.shape,
            use_shadow_buffer,
            handle
            )
        # set the buffer's data
        buffer.bind()
        GL.glBufferData( buffer.target, buffer.nbytes, None, buffer.usage )
        buffer[:] = np_object
        buffer.unbind()

        return buffer

    def __init__(
        self,
        target,
        usage,
        dtype,
        shape,
        use_shadow_buffer = False,
        handle = None,
        offset = 0,
        strides = None
        ):
        super( VertexBuffer, self ).__init__()

        self._target = target
        self._usage = usage
        self._dtype = numpy.dtype( dtype )
        self._shape = shape
        self._shadow_buffer = None
        self._offset = offset
        self._strides = tuple( strides ) if strides else ( self._dtype.itemsize, )

        if use_shadow_buffer:
            self._shadow_buffer = numpy.empty( self._shape, self._dtype )

        # create or copy the buffer handle
        self._handle = handle if handle else GL.glGenBuffers( 1 )

    @property
    def handle( self ):
        return self._handle

    @property
    def target( self ):
        return self._target

    @property
    def usage( self ):
        return self._usage

    @property
    def nbytes( self ):
        # nbytes = shape * dtype.itemsize
        return reduce( lambda x, y: x * y, self._shape ) * self._dtype.itemsize

    @property
    def dtype( self ):
        return self._dtype

    @dtype.setter
    def dtype( self, _dtype ):
        # validate the shape
        # throw ValueError if shape changes size
        new_size = reduce( lambda x, y: x * y, self._shape ) * _dtype.itemsize
        if self.nbytes != new_size:
            raise ValueError( "New dtype would change the buffer's size" )

        if None == self._shadow_buffer:
            self._dtype = _dtype

            # update the shape
            # dtype can change the view of the memory
            # if the size of dtype has changed, the shape should be updated

            shape = list( self.shape )

            # calculate the new number of elements in the buffer
            count = self.nbytes / self._dtype.itemsize
            # determine how many instances there are of the last dimension
            num_groups = reduce( lambda x, y: x * y, self._shape ) / self._shape[ -1 ]
            # update the last dimensions count to the number of values per instance
            shape[-1] = count / num_groups

            self.shape = tuple( shape )
        else:
            self._shadow_buffer.dtype = _dtype

    @property
    def shape( self ):
        return self._shape

    @shape.setter
    def shape( self, _shape ):
        # validate the shape
        # throw ValueError if shape changes size
        new_size = reduce( lambda x, y: x * y, _shape ) * self._dtype.itemsize
        if self.nbytes != new_size:
            raise ValueError( "New shape would change the buffer's size" )

        if None == self._shadow_buffer:
            self._shape = _shape
        else:
            self._shadow_buffer.shape = _shape

    @property
    def ndim( self ):
        return len( self._shape )

    @property
    def offset( self ):
        return self._offset

    @property
    def strides( self ):
        return self._strides

    @property
    def bound( self ):
        """Returns the bind state of the buffer.

        :rtype: boolean
        :return: Returns True if the buffer is currently bound.
        """
        return VertexBuffer.bound_buffer( self.target ) == self.handle

    @property
    def shadow_buffer( self ):
        """Returns the shadow buffer.

        This can be used to perform multiple operations before
        pushing them to OpenGL.
        """
        return self._shadow_buffer

    @property
    def attribute( self ):
        # return a data view of the buffer
        return VertexBuffer.Attribute( self )

    def __getitem__( self, index ):
        """Returns the selected data from the buffer.

        The data will be retreived from OpenGL before having
        the index applied to it and returned.

        If a shadow buffer is present, the data will be retrieved
        from the shadow buffer instead of from OpenGL.
        The buffer does *not* need to be bound if there is a shadow buffer.

        .. note: The shadow buffer may have un-pushed changes in it.
            Therefore, data retrieved may not be representative of
            the current buffer if a shadow buffer is present.

        :raise ValueError: Raised if there is no shadow buffer and the
            buffer is not bound.
        """
        # check if we have a shadow buffer
        if None != self._shadow_buffer:
            # we have a shadow buffer
            # just return the shadow buffer values
            return self._shadow_buffer[ index ]

        # no shadow buffer
        # we have to get the data from opengl
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        # TODO: this just gets the whole array
        # then gets the data from the indices
        # we need to be more efficient about this

        # get the data from opengl
        data = numpy.empty( self.shape, self.dtype )
        GL.glGetBufferSubData(
            self.target,
            0,
            self.nbytes,
            data
            )
        return data[ index ]

    def __setitem__( self, index, data ):
        """Updates the buffer with the provided data.

        The relevant sections of the buffer will be retrieved
        from OpenGL, updated, and passed back.

        If no stride is requested, the data will be set without
        needing to retrieve the data.
        For example::

            buffer[:] = [ 1.0, 2.0, 3.0 ]
            buffer[0:1] = [ 1.0 ]

        If a shadow buffer is present, data will not be requested from
        OpenGL before setting.
        Instead the shadow buffer will be updated and then the
        entire shadow buffer will be pushed.

        :raise ValueError: Raised if the buffer is not bound.
        """
        # the buffer must be bound
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        # check if we're receiving a shader attribute
        if isinstance( data, ShaderAttribute ):
            # redirect to our attribute helper
            self.attribute[ index ] = data
            return

        # check for a shadow buffer
        if None != self._shadow_buffer:
            # we have a shadow buffer
            # assign the data to the shadow buffer
            # then push the shadow buffer into opengl
            self._shadow_buffer[ index ] = data

            # TODO: pass 'index' to push function
            self.push_shadow_buffer()
            return

        # no shadow buffer

        # check if we're setting data without strides
        # this includes [:]
        # which means we can avoid the get
        if isinstance( index, slice ):
            # we check this by seeing if:
            # the start is 0
            # the end is >= nbytes
            # the stride is 1 or None
            if \
                index.step == 1 or \
                index.step == None:
                # get the slice start and stop
                # handle [:] slice which is (None,None,None)
                start = index.start * self._dtype.itemsize if index.start else 0
                stop = index.stop * self._dtype.itemsize if index.stop else self.nbytes

                # push back into opengl
                GL.glBufferSubData( self.target, start, stop, data )
                return

        # the data has strides or is a list of slices
        # we have to get the data from opengl
        # then we update the data and pass it back

        # TODO: this gets and sets the entire buffer
        # we should try and get as smaller chunk as possible

        # get the data
        buffer_data = self[:]
        # update our slice values
        buffer_data[ index ] = data
        # push back into opengl
        GL.glBufferSubData(
            self.target,
            0,
            self.nbytes,
            buffer_data
            )

    def push_shadow_buffer( self ):
        """Pushes the current shadow buffer to the OpenGL buffer.

        This allows you to perform multiple operations on the
        shadow buffer before the final result is pushed.
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        # push entire buffer
        GL.glBufferSubData(
            self.target,
            0,
            self.nbytes,
            self._shadow_buffer
            )

    def bind( self ):
        """Binds the current buffer.

        This will activate the buffer.

        Asserts that the buffer is not currently bound.
        """
        if self.bound:
            raise ValueError( "Buffer is already bound" )
        GL.glBindBuffer( self.target, self.handle )

    def unbind( self ):
        """Unbinds the current buffer.

        This will deactivate the buffer.

        Asserts that the buffer is currently bound.
        """
        if not self.bound:
            raise ValueError( "Buffer is not bound" )
        GL.glBindBuffer( self.target, 0 )


    def set_attribute(
        self,
        location,
        values_per_vertex = 1,
        normalise = False,
        glType = None
        ):
        """Sets the attribute pointer.

        This is the equivalent of calling glVertexAttribPointer.

        This function automatically handles a quirk in PyOpenGL
        where an offset of 0 must be specified as None.
        """
        normalise = GL.GL_TRUE if normalise else GL.GL_FALSE
        offset = ctypes.c_void_p( self._offset ) if self._offset else None

        # TODO: this won't work for all cases
        glType = glType if glType else numpy_utils.dtype_type( self.dtype )
        stride = self._stride[ 0 ]

        GL.glVertexAttribPointer(
            location,
            values_per_vertex,
            glType,
            normalise,
            stride,
            offset
            )

    def __str__( self ):
        string = \
            "%s:\n" \
            "nbytes:\t%s"  % (
                self.__class__.__name__,
                self.nbytes
                )
        return string

