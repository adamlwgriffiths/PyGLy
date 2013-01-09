
class FBO( object ):

    def __init__( self ):
        super( FBO, self ).__init__()

        self.fbo = (GLuint)()
        glGenFramebuffers( 1, self.fbo )

        self.textures = {}

    def __del__( self ):
        fbo = getattr( self, 'fbo', None )
        if fbo:
            glDeleteFramebuffers( 1, fbo )

    def bind( self ):
        glBindFramebuffer( GL_RENDERBUFFER, self.fbo )

    def unbind( self ):
        glBindFramebuffer( GL_RENDERBUFFER, 0 )

    def set_active( self, targets = None ):
        """Prepares the FBO for drawing.
        Calls glDrawFramebuffer.

        If targets is None, the entire set of
        currently set texture targets will be used.
        """
        if not targets:
            targets = self.textures.keys()

        enums = numpy.array([targets])
        data = (GLuint * enums.size)(*enums.flat)

        glDrawFramebuffer( enums.size, data )

    def attach_texture_2d(
        self,
        texture,
        texture_target = GL_TEXTURE_2D,
        fb_target = GL_COLOR_ATTACHMENT0,
        level = 0,
        ):
        glFramebufferTexture2d(
            GL_FRAMEBUFFER,
            fb_target,
            texture_target,
            texture,
            level
            )
        self.textures[ fb_target ] = texture

class ManagedFBO( FBO ):
    def create_texture_2d( self ):
        pass
    pass

