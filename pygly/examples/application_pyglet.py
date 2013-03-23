import pyglet

import pygly.gl
import pygly.pyglet_monkey_patch

from application import BaseApplication

# disable the shadow window
# this uses a legacy profile and causes issues
# on OS-X
pyglet.options['shadow_window'] = False

# over-ride the default pyglet idle loop
pygly.pyglet_monkey_patch.patch_idle_loop()

# patch pyglet's OpenGL legacy code out
pygly.pyglet_monkey_patch.patch_window_for_opengl_core()


class Application( BaseApplication ):

    keys = {
        pyglet.window.key.UP:       "up",
        pyglet.window.key.DOWN:     "down",
        pyglet.window.key.LEFT:     "left",
        pyglet.window.key.RIGHT:    "right",
        }

    def __init__( self, scene ):
        """Sets up the core functionality we need
        to begin rendering.
        This includes the OpenGL configuration, the
        window, the viewport, the event handler
        and update loop registration.
        """
        super( Application, self ).__init__( scene )

        if self.scene.core_profile:
            gl_config = pyglet.gl.Config(
                depth_size = 24,
                double_buffer = True,
                major_version = 3,
                minor_version = 2,
                forward_compatible = True,
                )
        else:
            # setup our opengl requirements
            gl_config = pyglet.gl.Config(
                depth_size = 24,
                double_buffer = True,
                )

        # create our window
        self.window = pyglet.window.Window(
            fullscreen = False,
            width = 1024,
            height = 768,
            resizable = True,
            vsync = False,
            config = gl_config,
            )

        # listen for draw and resize events
        self.window.push_handlers(
            on_draw = self.render,
            on_resize = self.on_window_resized,
            on_key_press = self.on_key_press,
            on_key_release = self.on_key_release
            )

        # set the window caption
        self.window.set_caption( "PyGLy - Pyglet - " + scene.name )

        # use a pyglet callback for our render loop
        pyglet.clock.schedule( self.step )

        # print some opengl information
        pygly.gl.print_gl_info()

        # create the scene now that we've got our window open
        self.scene.initialise()

        # resize the viewports
        self.on_window_resized( self.window.width, self.window.height )

    def run( self ):
        """Begins the Pyglet main loop.
        """
        pyglet.app.run()

    def on_key_press( self, key, modifiers ):
        # check the key value against known ranges
        if key >= pyglet.window.key.A and key <= pyglet.window.key.Z:
            # use the key as ascii
            self.scene.on_key_pressed( key )
        else:
            # for values outsize the ascii range, we need to manually convert them
            if key in self.keys:
                self.scene.on_key_pressed( self.keys[ key ] )

    def on_key_release( self, key, modifiers ):
        # check the key value against known ranges
        if key >= pyglet.window.key.A and key <= pyglet.window.key.Z:
            # use the key as ascii
            self.scene.on_key_released( key )
        else:
            # for values outsize the ascii range, we need to manually convert them
            if key in self.keys:
                self.scene.on_key_released( self.keys[ key ] )

    def on_window_resized( self, width, height ):
        """Called when the window is resized.

        We need to update our projection matrix with respect
        to our viewport size, or the content will become
        skewed.
        """
        self.scene.on_window_resized( width, height )

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
        super( Application, self ).step( dt )

        # manually dispatch the on_draw event
        # as we patched it out of the idle loop
        self.window.dispatch_event( 'on_draw' )

        # display the frame buffer
        self.window.flip()

