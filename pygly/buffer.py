"""
TODO: get gl buffer limit values
"""

import ctypes

from OpenGL import GL

from pyrr.utils import \
	all_parameters_as_numpy_arrays, \
	parameters_as_numpy_arrays

class Buffer( object ):

	valid_usage = set(
		[
			GL.GL_STATIC_DRAW,
			GL.GL_STATIC_READ,
			GL.GL_STATIC_COPY,
			GL.GL_STREAM_DRAW,
			GL.GL_STREAM_READ,
			GL.GL_STREAM_COPY,
			GL.GL_DYNAMIC_DRAW,
			GL.GL_DYNAMIC_READ,
			GL.GL_DYNAMIC_COPY,
			]
		)
	valid_access = set(
		[
			GL.GL_READ_ONLY,
			GL.GL_WRITE_ONLY,
			GL.GL_READ_WRITE,
			]
		)

	def __init__( self, target = GL.GL_ARRAY_BUFFER, usage = GL.GL_STATIC_DRAW ):
		super( Buffer, self ).__init__()

		if usage not in Buffer.valid_usage:
			raise ValueError( "Not a valid buffer usage type" )

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
		if usage not in Buffer.valid_usage:
			raise ValueError( "Not a valid buffer usage type" )

		self._usage = usage
		self._nbytes = nbytes

		GL.glBufferData( self.target, self.nbytes, None, self.usage )

	@parameters_as_numpy_arrays( 'data' )
	def set_data( self, data, usage = None ):
		if usage:
			if usage not in Buffer.valid_usage:
				raise ValueError( "Not a valid buffer usage type" )

			self._usage = usage

		self._nbytes = data.nbytes

		GL.glBufferData( self.target, self.nbytes, data, self.usage )

	@parameters_as_numpy_arrays( 'data' )
	def set_sub_data( self, data, offset = 0 ):
		cbyte_offset = ctypes.c_void_p(offset)
		GL.glBufferSubData( self.target, cbyte_offset, data.nbytes, data )

	def map( self, access = GL.GL_READ_WRITE ):
		if access not in valid_access:
			raise ValueError( "Not a valid buffer access type" )

		return GL.glMapBuffer( self.target, access )

	def unmap( self ):
		GL.glUnmapBuffer( self.target )

