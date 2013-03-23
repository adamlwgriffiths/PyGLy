import textwrap

from OpenGL import GL


class Scene( object ):

    def __init__( self, core_profile = True ):
        super( Scene, self ).__init__()

        self.core_profile = core_profile

    @property
    def name( self ):
        return "Scene"

    def initialise( self ):
        pass

    def on_key_pressed( self, key ):
        pass

    def on_key_released( self, key ):
        pass

    def on_window_resized( self, width, height ):
        pass

    def step( self, delta ):
        pass

    def render( self ):
        # just clear the buffer by default
        GL.glClearColor( 0.2, 0.2, 0.2, 1.0 )
        GL.glClear( GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT )

