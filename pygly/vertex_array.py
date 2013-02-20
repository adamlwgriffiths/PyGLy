from OpenGL import GL
import ctypes


class VertexArray( object ):

	def __init__(
		self,
		target = GL.GL_ARRAY_BUFFER,
		usage = GL.GL_STATIC_DRAW
		):
		super( VertexArray, self ).__init__()

		self._handle = GL.glGenVertexArrays( 1 )

	@property
	def handle( self ):
		return self._handle

	def bind( self ):
		GL.glBindVertexArray( self.handle )

	def unbind( self ):
		GL.glBindVertexArray( 0 )

	def enable_shader_attribute( self, shader, attribute ):
		location = shader.attributes[ attribute ]
		self.enable_attribute( location )

	def disable_shader_attribute( self, shader, attribute ):
		location = shader.attributes[ attribute ]
		self.disable_attribute( location )

	def enable_attribute( self, index ):
		GL.glEnableVertexAttribArray( index )

	def disable_attribute( self, index ):
		GL.glDisableVertexAttribArray( index )

	def set_attribute( self, index, values_per_vertex, type, stride = 0, offset = 0, normalise = False ):
		if offset == 0:
			offset = None
		else:
			offset = ctypes.c_void_p( offset )

		GL.glVertexAttribPointer(
			index,
			values_per_vertex,
			type,
			GL.GL_TRUE if normalise else GL.GL_FALSE,
			stride,
			offset
			)
