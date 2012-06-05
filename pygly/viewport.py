'''
Created on 22/06/2012

@author: adam
'''

import sys
import weakref

import numpy
from pyglet.event import EventDispatcher
from pyglet.gl import *

from pyrr import rectangle
from pyrr import geometric_tests
import gl
import window


class Viewport( EventDispatcher ):
    """
    A wrapper around the viewport functionality.
    """
    
    
    def __init__( self, window, rect ):
        """
        Creates a viewport with the size of rect.

        @param rect: An array with the shape (2,2).
        Values are in pixels
        Values may exceed the window size but will be off the screen.
        OpenGL may place limits on how far off screen a viewport
        may go.
        """
        super( Viewport, self ).__init__()

        self.window = window
        self._rect = numpy.array(
            rect,
            dtype = numpy.int
            )

        if self._rect.shape != (2,2):
            raise ValueError(
                "Viewport rect must be an array with shape (2,2)"
                )

        # listen for resize events
        window.push_handlers(
            on_resize = self.on_resize
            )

    @property
    def rect( self ):
        return self._rect

    @rect.setter
    def rect( self, rect ):
        if numpy.array_equal( self._rect, rect ):
            return

        self._rect[:] = rect

        # dispatch our events
        self.dispatch_event(
            'on_resize',
            self.rect
            )
        self.dispatch_event(
            'on_change_aspect_ratio',
            self.aspect_ratio
            )

    def on_resize( self, width, height ):
        """
        Called when the window is resized.
        """
        # we don't do anything by default
        pass
    
    def switch_to( self ):
        """
        Calls glViewport which sets up the viewport
        for rendering.

        @see pygly.gl.set_viewport.
        """
        # update our viewport size
        gl.set_viewport( self.rect )

    @property
    def aspect_ratio( self ):
        """
        Returns the aspect ratio of the viewport.

        Aspect ratio is the ratio of width to height
        a value of 2.0 means width is 2*height
        """
        return window.aspect_ratio( self.rect )

    def scissor_to_viewport( self ):
        """
        Calls glScissor with the size of the viewport.

        It is up to the user to call
        glEnable(GL_SCISSOR_TEST).

        @see pygly.gl.set_scissor.
        """
        gl.set_scissor( self.rect )
    
    def push_viewport_attributes( self ):
        """
        Pushes the current OGL attributes
        and then calls self.setup_viewport.
        """
        glPushAttrib( GL_ALL_ATTRIB_BITS )
        self.setup_viewport()

    def pop_viewport_attributes( self ):
        """
        Pops the OGL attributes.
        Called when tearing down viewport.
        This method mirrors 'push_viewport_attributes'
        """
        glPopAttrib()

    def setup_viewport( self ):
        """
        Over-ride this method to customise
        the opengl settings for this viewport.

        The default method sets the following:
        -glEnable( GL_DEPTH_TEST )
        -glShadeModel( GL_SMOOTH )
        -glEnable( GL_RESCALE_NORMAL )
        -glEnable( GL_SCISSOR_TEST )
        """
        # enable some default options
        # use the z-buffer when drawing
        glEnable( GL_DEPTH_TEST )

        # enable smooth shading
        glShadeModel( GL_SMOOTH )

        # because we use glScale for scene graph
        # scaling, normals will get affected too.
        # GL_RESCALE_NORMAL applies the inverse
        # value of the current matrice's scale
        # this is new in OGL1.2 and SHOULD be
        # faster than glEnable( GL_NORMALIZE )
        # http://www.opengl.org/archives/resources/features/KilgardTechniques/oglpitfall/
        glEnable( GL_RESCALE_NORMAL )

        # enable GL_SCISSOR_TEST so we can selectively
        # clear areas of the window
        glEnable( GL_SCISSOR_TEST )

    def create_viewport_point_from_window_point( self, point ):
        """
        Converts a point relative to the window, to a point
        relative to the viewport.

        @param window: The window that contains the viewport
        and point.
        @param viewport: The viewport the point is within.
        @param point: The point on the window. This is in pixels.
        @return: The point within the viewport.
        """
        # convert to viewport co-ordinates
        return numpy.array(
            [
                point[ 0 ] - self.rect[ 0 ][ 0 ],
                point[ 1 ] - self.rect[ 0 ][ 1 ]
                ],
            dtype = numpy.int
            )

    def create_window_point_from_viewport_point( self, point ):
        return numpy.array(
            [
                point[ 0 ] + self.rect[ 0 ][ 0 ],
                point[ 1 ] + self.rect[ 0 ][ 1 ]
                ],
            dtype = numpy.int
            )
        pass

    @property
    def x( self ):
        return self.left

    @property
    def y( self ):
        return self.bottom
    
    @property
    def width( self ):
        return rectangle.width( self.rect )
    
    @property
    def height( self ):
        return rectangle.height( self.rect )

    @property
    def left( self ):
        return rectangle.left( self.rect )

    @property
    def bottom( self ):
        return rectangle.bottom( self.rect )

    @property
    def right( self ):
        return rectangle.right( self.rect )

    @property
    def top( self ):
        return rectangle.top( self.rect )

    # document our events
    if hasattr( sys, 'is_epydoc' ):
        def on_resize( rect ):
            '''The viewport size was changed.

            :event:
            '''
        def on_change_aspect_ratio( aspect_ratio ):
            '''The viewport size was changed.

            :event:
            '''

# register our custom events
Viewport.register_event_type( 'on_resize' )
Viewport.register_event_type( 'on_change_aspect_ratio' )

