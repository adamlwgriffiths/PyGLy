from fps_monitor import FPS_Monitor

class BaseApplication( object ):


    def __init__( self, scene ):
        """Sets up the core functionality we need
        to begin rendering.
        This includes the OpenGL configuration, the
        window, the viewport, the event handler
        and update loop registration.
        """
        super( BaseApplication, self ).__init__()

        self.fps_monitor = FPS_Monitor()
        self.scene = scene

    def run( self ):
        """Begins the Pyglet main loop.
        """
        pass

    def step( self, dt ):
        """Updates our scene and triggers the on_draw event.
        
        This is scheduled in our __init__ method and
        called periodically by pyglet's event callbacks.
        We need to manually call 'on_draw' as we patched
        it our of pyglets event loop when we patched it
        out with pygly.monkey_patch.
        Because we called 'on_draw', we also need to
        perform the buffer flip at the end.

        Calls the scene's 'step' method, dispatches the pyglet
        'on_draw' event, then flips the pyglet buffer.
        """
        self.scene.step( dt )
        self.fps_monitor.increment_frame()

    def render( self ):
        """Triggered when pyglet's 'on_draw' event is fired.

        Calls the scene's render function.
        """
        self.scene.render()

