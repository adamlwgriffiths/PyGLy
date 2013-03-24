from time import time
import sys

import pygly.gl
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT

from application import BaseApplication


class Application( BaseApplication ):


    keys = {
        GLUT.GLUT_KEY_UP:    "up",
        GLUT.GLUT_KEY_DOWN:  "down",
        GLUT.GLUT_KEY_LEFT:  "left",
        GLUT.GLUT_KEY_RIGHT: "right",
        }

    ESCAPE = '\033'


    def __init__( self, scene ):
        """Sets up the core functionality we need
        to begin rendering.
        This includes the OpenGL configuration, the
        window, the viewport, the event handler
        and update loop registration.
        """
        super( Application, self ).__init__( scene )

        if self.scene.core_profile:
            raise ValueError( "GLUT does not support Core profile" )

        # glut initialization
        GLUT.glutInit( sys.argv )
        GLUT.glutInitDisplayMode( GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH )

        # set the window's dimensions
        GLUT.glutInitWindowSize( 1024, 768 )

        # set the window caption
        # create our window
        GLUT.glutCreateWindow( "PyGLy - GLUT - " + scene.name )

        # print some opengl information
        pygly.gl.print_gl_info()

        # create the scene now that we've got our window open
        self.scene.initialise()

        self.last_time = time()

        # set the function to draw
        GLUT.glutReshapeFunc( self.on_window_resized )
        GLUT.glutIdleFunc( self.idle )
        GLUT.glutDisplayFunc( self.render )
        GLUT.glutKeyboardFunc( self.on_key_pressed )
        GLUT.glutKeyboardUpFunc( self.on_key_released )
        GLUT.glutSpecialFunc( self.on_special_key_pressed )
        GLUT.glutSpecialUpFunc( self.on_special_key_released )

    def on_key_pressed( self, key, x, y ):
        # x and y is mouse when key was pressed
        if key == self.ESCAPE:
            sys.exit()

        self.scene.on_key_pressed( key )

    def on_key_released( self, key, x, y ):
        self.scene.on_key_released( key )

    def on_special_key_pressed( self, key, x, y ):
        if key in self.keys:
            self.scene.on_key_pressed( self.keys[ key ] )
            print self.keys[ key ]

    def on_special_key_released( self, key, x, y ):
        if key in self.keys:
            self.scene.on_key_released( self.keys[ key ] )

    def on_window_closed( self ):
        pass

    def run( self ):
        # start the mainloop
        GLUT.glutMainLoop()

    def on_window_resized( self, width, height ):
        """Called when the window is resized.

        We need to update our projection matrix with respect
        to our viewport size, or the content will become
        skewed.
        """
        self.scene.on_window_resized( width, height )

    def idle( self ):
        # get time
        current_time = time()
        delta = current_time - self.last_time
        self.last_time = current_time

        self.step( delta )

        GLUT.glutPostRedisplay()

    def render( self ):
        super( Application, self ).render()
        GLUT.glutSwapBuffers()
