'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
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
    """A wrapper around the basic viewport functionality.
    """
    
    
    def __init__( self, window, rect ):
        """Creates a viewport with the size of rect.

        Automatically hooks into the window's 'on_resize'
        event.

        Args:
            window: The window the viewport belongs to.
            rect: An array with the shape (2,2).
            Values are in pixels
            Values may exceed the window size but will be
            off the screen.

        .. note::
            OpenGL places platform-dependent limits on how far
            off screen a viewport may go.
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
        """The viewports 2D rectangle in pixels.

        .. note:: Changing this value will dispatch an
        'on_viewport_resize' and 'on_change_aspect_ratio'
        events.

        Returns:
            The viewport size in pixels in the form of a
            NumPy with shape (2,2).
        """
        return self._rect

    @rect.setter
    def rect( self, rect ):
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed

        self._rect[:] = rect

        # dispatch our events
        self.dispatch_event(
            'on_viewport_resize',
            self.rect
            )
        self.dispatch_event(
            'on_change_aspect_ratio',
            self.aspect_ratio
            )

    def on_resize( self, width, height ):
        """Event handler for pyglet window's on_resize
        event.
        
        Called when the window is resized.

        This is a stub function and is intended to be
        over-ridden.
        """
        # we don't do anything by default
        pass
    
    def switch_to( self ):
        """Calls glViewport which sets up the viewport
        for rendering.

        .. seealso::
            Function :py:func:`pygly.gl.set_viewport`
            Documentation of the
            :py:func:`pygly.gl.set_viewport` function.
        """
        # update our viewport size
        gl.set_viewport( self.rect )

    def __enter__( self ):
        # activate our viewport
        # scissor to the viewport
        # and set our gl state
        self.switch_to()
        self.scissor_to_viewport()
        self.push_viewport_attributes()

    def __exit__( self, type, value, traceback ):
        # pop our gl state
        # reset our scissor
        # and reset our viewport to full size
        self.pop_viewport_attributes()
        window_rect = window.create_rectangle( self.window )
        gl.set_scissor( window_rect )
        gl.set_viewport( window_rect )

    @property
    def aspect_ratio( self ):
        """Returns the aspect ratio of the viewport.

        Aspect ratio is the ratio of width to height
        a value of 2.0 means width is 2*height

        .. note::
            This is an @property decorated method which allows
            retrieval and assignment of the scale value.
        """
        return window.aspect_ratio( self.rect )

    def scissor_to_viewport( self ):
        """Calls glScissor with the size of the viewport.

        .. note::
            It is up to the user to call glEnable(GL_SCISSOR_TEST).

        .. seealso::
            Function :py:func:`pygly.gl.set_scissor`
            Documentation of the
            :py:func:`pygly.gl.set_scissor` function.
        """
        gl.set_scissor( self.rect )

    def push_viewport_attributes( self ):
        """Pushes the current OGL attributes
        and then calls self.setup_viewport.
        """
        glPushAttrib( GL_ALL_ATTRIB_BITS )
        self.setup_viewport()

    def pop_viewport_attributes( self ):
        """Pops the OGL attributes.

        Called when tearing down viewport.

        .. note::
            This method mirrors 'push_viewport_attributes'
        """
        glPopAttrib()

    def setup_viewport( self ):
        """Sets the viewport rendering attributes.
        
        Over-ride this method to customise
        the opengl settings for this viewport.

        The default method sets the following:
            #. glEnable( GL_DEPTH_TEST )
            #. glShadeModel( GL_SMOOTH )
            #. glEnable( GL_RESCALE_NORMAL )
            #. glEnable( GL_SCISSOR_TEST )
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

        # enable back face culling
        glEnable( GL_CULL_FACE )
        glCullFace( GL_BACK )

    @property
    def x( self ):
        """The X value of the viewport in pixels.

        This is the X value of the bottom left corner.
        """
        return self.left

    @property
    def y( self ):
        """The Y value of the viewport in pixels.

        This is the Y value of the bottom left corner.
        """
        return self.bottom

    @property
    def size( self ):
        """The size of the viewport in pixels as a 2D vector.
        """
        return rectangle.size( self.rect )

    @property
    def position( self ):
        """The origin of the viewport in pixels as a 2D vector.

        This is the bottom left corner.
        """
        return rectangle.position( self.rect )
    
    @property
    def width( self ):
        """The width of the viewport in pixels.
        """
        return rectangle.width( self.rect )
    
    @property
    def height( self ):
        """The height of the viewport in pixels.
        """
        return rectangle.height( self.rect )

    @property
    def left( self ):
        """The left most point of the viewport in pixels.
        """
        return rectangle.left( self.rect )

    @property
    def bottom( self ):
        """The bottom most point of the viewport in pixels.
        """
        return rectangle.bottom( self.rect )

    @property
    def right( self ):
        """The right most point of the viewport in pixels.
        """
        return rectangle.right( self.rect )

    @property
    def top( self ):
        """The top most point of the viewport in pixels.
        """
        return rectangle.top( self.rect )

    # document our events
    if hasattr( sys, 'is_epydoc' ):
        def on_viewport_resize( rect ):
            '''The viewport size was changed.

            :event:
            '''
        def on_change_aspect_ratio( aspect_ratio ):
            '''The viewport size was changed.

            :event:
            '''

# register our custom events
Viewport.register_event_type( 'on_viewport_resize' )
Viewport.register_event_type( 'on_change_aspect_ratio' )

