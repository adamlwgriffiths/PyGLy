from time import time

import pygly.gl
import glfw
import OpenGL.GL as GL

from application import BaseApplication


class Application( BaseApplication ):

    keys = {
        glfw.KEY_UP:    "up",
        glfw.KEY_DOWN:  "down",
        glfw.KEY_LEFT:  "left",
        glfw.KEY_RIGHT: "right",
        }


    def __init__( self, scene ):
        """Sets up the core functionality we need
        to begin rendering.
        This includes the OpenGL configuration, the
        window, the viewport, the event handler
        and update loop registration.
        """
        super( Application, self ).__init__( scene )

        glfw.Init()

        if self.scene.core_profile:
            glfw.OpenWindowHint( glfw.OPENGL_VERSION_MAJOR, 3 )
            glfw.OpenWindowHint( glfw.OPENGL_VERSION_MINOR, 2 )
            glfw.OpenWindowHint( glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE )
            glfw.OpenWindowHint( glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE )

        # create our window
        glfw.OpenWindow(
            1024, 768,
            8, 8, 8,
            8, 24, 0,
            glfw.WINDOW
            )

        # set the window caption
        glfw.SetWindowTitle( "PyGLy - PyGLFW - " + scene.name )

        # print some opengl information
        pygly.gl.print_gl_info()

        # create the scene now that we've got our window open
        self.scene.initialise()

        self.running = False

        # listen for resize events and close window events
        # do this AFTER initialising the scene
        # as the window size callback will trigger once set
        glfw.SetWindowSizeCallback( self.on_window_resized )
        glfw.SetWindowCloseCallback( self.on_window_closed )
        glfw.SetKeyCallback( self.on_key_event )

    def on_key_event( self, key, action ):
        if action == glfw.GLFW_PRESS:
            func = self.scene.on_key_pressed
        else:
            func = self.scene.on_key_released

        # check the key value against known ranges
        if key < glfw.KEY_SPECIAL:
            # use the key as ascii
            func( key )
        else:
            # the key is a special key
            # we need to know which ones we're using
            if key in self.keys:
                func( self.keys[ key ] )

    def on_window_closed( self ):
        self.running = False

    def run( self ):
        self.running = True
        last_time = time()
        while self.running:
            if glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS:
                self.running = False
                break

            # get time
            current_time = time()
            delta = current_time - last_time
            last_time = current_time
            self.step( delta )
            self.render()
            
            glfw.SwapBuffers()

    def on_window_resized( self, width, height ):
        """Called when the window is resized.

        We need to update our projection matrix with respect
        to our viewport size, or the content will become
        skewed.
        """
        self.scene.on_window_resized( width, height )

