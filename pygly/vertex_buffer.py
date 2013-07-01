import ctypes

from OpenGL import GL

from pyrr.utils import parameters_as_numpy_arrays

from pygly.gl import enum_to_type, _generate_enum_map
from pygly.shader import Attribute



class VertexBuffer( object ):

    _target_string_map = _generate_enum_map(
        {
            "GL_ARRAY_BUFFER":          "GL_ARRAY_BUFFER",
            "GL_TEXTURE_BUFFER":        "GL_TEXTURE_BUFFER",
            "GL_ELEMENT_ARRAY_BUFFER":  "GL_ELEMENT_ARRAY_BUFFER",
            "GL_ATOMIC_COUNTER_BUFFER": "GL_ATOMIC_COUNTER_BUFFER",
            "GL_COPY_READ_BUFFER":      "GL_COPY_READ_BUFFER",
            "GL_COPY_WRITE_BUFFER":     "GL_COPY_WRITE_BUFFER",
            "GL_DRAW_INDIRECT_BUFFER":  "GL_DRAW_INDIRECT_BUFFER",
            "GL_DISPATCH_INDIRECT_BUFFER":  "GL_DISPATCH_INDIRECT_BUFFER",
            "GL_PIXEL_PACK_BUFFER":     "GL_PIXEL_PACK_BUFFER",
            "GL_PIXEL_UNPACK_BUFFER":   "GL_PIXEL_UNPACK_BUFFER",
            "GL_SHADER_STORAGE_BUFFER": "GL_SHADER_STORAGE_BUFFER",
            "GL_TRANSFORM_FEEDBACK_BUFFER": "GL_TRANSFORM_FEEDBACK_BUFFER",
            "GL_UNIFORM_BUFFER":        "GL_UNIFORM_BUFFER",
            }
        )

    _usage_string_map = _generate_enum_map(
        {
            "GL_STREAM_DRAW":           "GL_STREAM_DRAW",
            "GL_STREAM_READ":           "GL_STREAM_READ",
            "GL_STREAM_COPY":           "GL_STREAM_COPY",
            "GL_STATIC_DRAW":           "GL_STATIC_DRAW",
            "GL_STATIC_READ":           "GL_STATIC_READ",
            "GL_STATIC_COPY":           "GL_STATIC_COPY",
            "GL_DYNAMIC_DRAW":          "GL_DYNAMIC_DRAW",
            "GL_DYNAMIC_READ":          "GL_DYNAMIC_READ",
            "GL_DYNAMIC_COPY":          "GL_DYNAMIC_COPY",
            }
        )

    @staticmethod
    def target_to_string( target ):
        return VertexBuffer._target_string_map[ target ]

    @staticmethod
    def usage_to_string( usage ):
        return VertexBuffer._usage_string_map[ usage ]

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
        return VertexBuffer.bound_buffer( self.target ) == self.handle

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

    def get_data( self, offset = 0, nbytes = None ):
        """Returns the data currently in the buffer.

        :raise ValueError: Raised if the buffer is not currently bound.
        """
        if not nbytes:
            nbytes = self.nbytes

        if not self.bound:
            raise ValueError( "Buffer is not bound" )

        data = numpy.empty( self.buffer.shape, self.buffer.dtype )
        GL.glGetBufferSubData(
            self.buffer.target,
            offset,
            nbytes,
            data
            )
        return data

    def __str__( self ):
        return  "%s(target=%s, usage=%s, nbytes=%d)" % (
            self.__class__.__name__,
            VertexBuffer.target_to_string( self.target ),
            VertexBuffer.usage_to_string( self.usage ),
            self.nbytes
            )



class BufferAttributes( object ):

    def __init__( self ):
        super( BufferAttributes, self ).__init__()

        self.attributes = {}

    def __setitem__( self, index, item ):
        self.attributes[ index ] = item

    def __getitem__( self, index ):
        return self.attributes[ index ]

    def set( self, enable = True ):
        for name, attribute in self.attributes.items():
            attribute.set( enable )

    def push_attributes( self ):
        """Pushes the enable and pointer state of vertex arrays.

        This is used to store the state of the vertex attributes in OpenGL
        which can then be popped later to return the stack to a previous state.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glPushClientAttrib( GL.GL_CLIENT_VERTEX_ARRAY_BIT )

    def pop_attributes( self ):
        """Pops the enable and pointer state of vertex arrays.

        Returns the vertex attribute state to the state it was in when
        push_attributes was called.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glPopClientAttrib()



class BufferAttribute( object ):

    @classmethod
    def from_dtype( cls, buffer, dtype, name, offset = 0, **kwargs ):
        import numpy_utils

        args = {
            'buffer':   buffer,
            'values_per_vertex':    numpy_utils.dtype_element_count( dtype, name ),
            'gl_type':  numpy_utils.dtype_gl_enum( dtype, name ),
            'stride':   dtype.itemsize,
            'offset':   offset + numpy_utils.dtype_offset( dtype, name )
            }
        args.update( kwargs )

        return cls( **args )

    def __init__( self, buffer ):
        super( BufferAttribute, self ).__init__()

        self._buffer = buffer

    @property
    def buffer( self ):
        return self._buffer

    def set( self, enable = True ):
        raise NotImplementedError

    def enable( self ):
        raise NotImplementedError

    def disable( self ):
        raise NotImplementedError


class VertexAttribute( BufferAttribute ):

    def __init__(
        self,
        buffer,
        values_per_vertex = 3,
        gl_type = GL.GL_FLOAT,
        stride = None,
        offset = None,
        **kwargs
        ):
        super( VertexAttribute, self ).__init__( buffer, )

        self.values_per_vertex = values_per_vertex
        self.gl_type = gl_type
        
        # we need to get the size of the actual gl_type, not the GL enum
        gl_type_size = ctypes.sizeof( enum_to_type( self.gl_type ) )
        self.stride = stride if stride else self.values_per_vertex * gl_type_size

        self.offset = offset

    def set( self, enable = True ):
        # TODO: check if buffer is in VRAM or system RAM
        # if in system ram, don't check if bound!
        if not self.buffer.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable()

        offset = ctypes.c_void_p( self.offset ) if self.offset else None
        GL.glVertexPointer( self.values_per_vertex, self.gl_type, self.stride, offset )

    def enable( self ):
        """Enables the vertex position data for rendering.

        If vertex data is not enabled before rendering, the data
        will be ignored by OpenGL.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_VERTEX_ARRAY )

    def disable( self ):
        """Disables the vertex position data.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_VERTEX_ARRAY )


class ColourAttribute( BufferAttribute ):

    def __init__(
        self,
        buffer,
        values_per_vertex = 3,
        gl_type = GL.GL_FLOAT,
        stride = None,
        offset = None,
        **kwargs
        ):
        super( ColourAttribute, self ).__init__( buffer )

        self.values_per_vertex = values_per_vertex
        self.gl_type = gl_type

        # we need to get the size of the actual gl_type, not the GL enum
        gl_type_size = ctypes.sizeof( enum_to_type( self.gl_type ) )
        self.stride = stride if stride else self.values_per_vertex * gl_type_size

        self.offset = offset

    def set( self, enable = True ):
        """Sets the glColorPointer.

        .. note:: This function automatically handles a quirk in PyOpenGL
        where an offset of 0 must be specified as None.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        if not self.buffer.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable()

        offset = ctypes.c_void_p( self.offset ) if self.offset else None
        GL.glColorPointer( self.values_per_vertex, self.gl_type, self.stride, offset )

    def enable( self ):
        """Enables the vertex colour data for rendering.

        If vertex colour data is not enabled before rendering, the colour
        data will be ignored by OpenGL.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_COLOR_ARRAY )

    def disable( self ):
        """Disables the vertex colour data.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_COLOR_ARRAY )



class TextureCoordAttribute( BufferAttribute ):

    def __init__(
        self,
        buffer,
        values_per_vertex = 2,
        gl_type = GL.GL_FLOAT,
        stride = None,
        offset = None,
        **kwargs
        ):
        super( TextureCoordAttribute, self ).__init__( buffer )

        self.values_per_vertex = values_per_vertex
        self.gl_type = gl_type
        
        # we need to get the size of the actual gl_type, not the GL enum
        gl_type_size = ctypes.sizeof( enum_to_type( self.gl_type ) )
        self.stride = stride if stride else self.values_per_vertex * gl_type_size

        self.offset = offset

    def set( self, enable = True ):
        """Sets the glColorPointer.

        .. note:: This function automatically handles a quirk in PyOpenGL
        where an offset of 0 must be specified as None.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        if not self.buffer.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable()

        offset = ctypes.c_void_p( self.offset ) if self.offset else None
        GL.glTexCoordPointer( self.values_per_vertex, self.gl_type, self.stride, offset )

    def enable( self ):
        """Enables the vertex texture co-ordinate data for rendering.

        If vertex texture co-ordinate data is not enabled before rendering,
        the texture co-ordinate data will be ignored by OpenGL.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_TEXTURE_COORD_ARRAY )

    def disable( self ):
        """Disables the vertex texture co-ordinate data.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_TEXTURE_COORD_ARRAY )



class NormalAttribute( BufferAttribute ):

    def __init__(
        self,
        buffer,
        gl_type = GL.GL_FLOAT,
        stride = None,
        offset = None,
        **kwargs
        ):
        super( NormalAttribute, self ).__init__( buffer )

        self.gl_type = gl_type

        # we need to get the size of the actual gl_type, not the GL enum
        gl_type_size = ctypes.sizeof( enum_to_type( self.gl_type ) )
        self.stride = stride if stride else self.values_per_vertex * gl_type_size

        self.offset = offset

    def set( self, enable = True ):
        """Sets the glNormalPointer.

        .. note:: This function automatically handles a quirk in PyOpenGL
        where an offset of 0 must be specified as None.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        if not self.buffer.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable()

        offset = ctypes.c_void_p( self.offset ) if self.offset else None
        GL.glNormalPointer( self.gl_type, self.stride, offset )

    def enable( self ):
        """Enables the vertex normal data for rendering.

        If vertex normal data is not enabled before rendering, the normal
        data will be ignored by OpenGL.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_NORMAL_ARRAY )

    def disable( self ):
        """Disables the vertex normal data.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_NORMAL_ARRAY )



class IndexAttribute( BufferAttribute ):

    def __init__(
        self,
        buffer,
        gl_type = GL.GL_UNSIGNED_INT,
        stride = None,
        offset = None,
        **kwargs
        ):
        super( IndexAttribute, self ).__init__( buffer )

        self.gl_type = gl_type

        # we need to get the size of the actual gl_type, not the GL enum
        gl_type_size = ctypes.sizeof( enum_to_type( self.gl_type ) )
        self.stride = stride if stride else self.values_per_vertex * gl_type_size

        self.offset = offset

    def set( self, enable = True ):
        """Sets the glNormalPointer.

        .. note:: This function automatically handles a quirk in PyOpenGL
        where an offset of 0 must be specified as None.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        if not self.buffer.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable()

        offset = ctypes.c_void_p( self.offset ) if self.offset else None
        GL.glIndexPointer( gl_type, stride, offset )

    def enable( self ):
        """Enables the vertex index data for rendering.

        If vertex index data is not enabled before rendering, the index
        data will be ignored by OpenGL and the vertices will be rendered
        as an ordered list.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glEnableClientState( GL.GL_INDEX_ARRAY )

    def disable( self ):
        """Disables the vertex index data.

        .. warning:: This function is removed from the OpenGL Core profile and **only**
            exists in OpenGL Legacy profile (OpenGL version <=2.1).
        """
        GL.glDisableClientState( GL.GL_INDEX_ARRAY )




class GenericAttribute( BufferAttribute ):

    def __init__(
        self,
        buffer,
        location,
        values_per_vertex = 3,
        gl_type = GL.GL_FLOAT,
        stride = None,
        offset = None,
        normalise = False,
        **kwargs
        ):
        super( GenericAttribute, self ).__init__( buffer )

        self.values_per_vertex = values_per_vertex
        self.gl_type = gl_type

        # we need to get the size of the actual gl_type, not the GL enum
        gl_type_size = ctypes.sizeof( enum_to_type( self.gl_type ) )
        self.stride = stride if stride else self.values_per_vertex * gl_type_size

        self.offset = offset
        self.location = location
        self.normalise = normalise

    def set( self, enable = True ):
        """Sets the attribute pointer.

        This is the equivalent of calling glVertexAttribPointer.

        This function automatically handles a quirk in PyOpenGL
        where an offset of 0 must be specified as None.

        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_attribute_pointer`
        .. seealso:: `py:func:pygly.vertex_buffer.Buffer.enable_shader_attribute_pointer`
        """
        if not self.buffer.bound:
            raise ValueError( "Buffer is not bound" )

        if enable:
            self.enable()

        # handle receiving shader attribute objects
        location = self.location
        if isinstance( location, Attribute ):
            location = location.location

        normalise = GL.GL_TRUE if self.normalise else GL.GL_FALSE
        offset = ctypes.c_void_p( self.offset ) if self.offset else None
        GL.glVertexAttribPointer(
            location,
            self.values_per_vertex,
            self.gl_type,
            normalise,
            self.stride,
            offset
            )

    def enable( self ):
        """Enables the attribute at the specified location.

        If vertex attribute data is not enabled before rendering, the attribute
        data will be ignored by OpenGL.

        :param pygly.shader.ShaderProgram shader: The shader object.
        :param string attribute: The attribute name to enable.
        """
        location = self.location
        if isinstance( location, Attribute ):
            location = location.location
        GL.glEnableVertexAttribArray( location )

    def disable( self ):
        """Disables the attribute at specified location.

        :param pygly.shader.ShaderProgram shader: The shader object.
        :param string attribute: The attribute name to disable.
        """
        location = self.location
        if isinstance( location, Attribute ):
            location = location.location
        GL.glDisableVertexAttribArray( location )

