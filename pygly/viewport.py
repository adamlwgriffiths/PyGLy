'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

import sys

import numpy
from pyglet.event import EventDispatcher
from pyglet.gl import *

from pyrr import rectangle
from pyrr import geometric_tests


def aspect_ratio( rect ):
    """Calculates the aspect ratio of the rectangle.

    Aspect ratio is the ratio of width to height
    a value of 2.0 means width is 2*height

    The rectangle is in the format of Pyrr.rectangle.

    Returns:
        The aspect ratio of the rectangle.
    """
    width = float(rectangle.abs_width(rect))
    height = float(rectangle.abs_height(rect))
    return width / height

def get_viewport():
    rect = (GLint * 4)()
    glGetIntegerv( GL_VIEWPORT, rect )
    return rectangle.create_from_position(
        x = rect[ 0 ],
        y = rect[ 1 ],
        width = rect[ 2 ],
        height = rect[ 3 ]
        )

def set_viewport( rect ):
    """Calls glViewport with the dimensions of
    the rectangle

    In the OpenGL Legacy profile (<=2.1),
    this call can be undone by first calling
    glPushAttrib( GL_VIEWPORT_BIT )
    and later calling glPopAttrib().
    Or: using the attribute context:
    with attributes( GL_VIEWPORT_BIT ):
        set_viewport( rect )

    These functions are not available on the
    OpenGL Core profile (>=3.0)
    """
    glViewport(
        int(rectangle.x_minimum(rect)),
        int(rectangle.y_minimum(rect)),
        int(rectangle.abs_width(rect)),
        int(rectangle.abs_height(rect))
        )

def get_scissor():
    rect = (GLint * 4)()
    glGetIntegerv( GL_SCISSOR_BOX, rect )
    return rectangle.create_from_position(
        x = rect[ 0 ],
        y = rect[ 1 ],
        width = rect[ 2 ],
        height = rect[ 3 ]
        )

def set_scissor( rect ):
    """Calls glScissor with the size of the rectangle.

    .. note:: It is up to the user to call glEnable(GL_SCISSOR_TEST).

    .. note:: To undo this, call this function again with the window's size as a rectangle.

    .. seealso::
        Module :py:mod:`pygly.window`
          Documentation of the :py:mod:`pygly.window` module.

    This call can be undone by first calling
    glPushAttrib( GL_SCISSOR_BIT )
    and later calling glPopAttrib().

    Or using the attribute context:
    with attributes( GL_SCISSOR_BIT ):
        set_scissor( rect )
    """
    glScissor(
        int(rectangle.x_minimum(rect)),
        int(rectangle.y_minimum(rect)),
        int(rectangle.abs_width(rect)),
        int(rectangle.abs_height(rect))
        )


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
            Function :py:func:`pygly.viewport.set_viewport`
            Documentation of the
            :py:func:`pygly.viewport.set_viewport` function.
        """
        # update our viewport size
        set_viewport( self.rect )

    @property
    def aspect_ratio( self ):
        """Returns the aspect ratio of the viewport.

        Aspect ratio is the ratio of width to height
        a value of 2.0 means width is 2*height

        .. note::
            This is an @property decorated method which allows
            retrieval and assignment of the scale value.
        """
        return aspect_ratio( self.rect )

    def scissor_to_viewport( self ):
        """Calls glScissor with the size of the viewport.

        .. note::
            It is up to the user to call glEnable(GL_SCISSOR_TEST).

        .. seealso::
            Function :py:func:`pygly.viewport.set_scissor`
            Documentation of the
            :py:func:`pygly.viewport.set_scissor` function.
        """
        set_scissor( self.rect )

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

    def __getitem__( self, key ):
        """Allow the viewport to be accessed as if
        it is an array
        """
        return self.rect[ key ]

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

