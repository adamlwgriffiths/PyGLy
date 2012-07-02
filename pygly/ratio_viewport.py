'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

import numpy

import pygly.window
from viewport import Viewport


class RatioViewport( Viewport ):
    """Maintains a set size ratio within a window.

    A RatioViewport will automatically resize itself when
    the window is resized, to maintain a specific ratio of
    the window size.
    """
    
    
    def __init__( self, window, ratio ):
        """Creates a viewport with the specified ratio.

        Automatically hooks into the window's 'on_resize'
        event.

        Args:
            window: The window the viewport belongs to.
            rect: The viewport size as a ratio (percentage)
            of the window in the form of a NumPy array
            with the shape (2,2).
            Values are in percentages (0.0 -> 1.0).
            Values may exceed the window size but will be off
            the screen.
        
        .. note::
            OpenGL places platform-dependent limits on how far
            off screen a viewport may go.
        """

        # we need self._rect to be valid
        # before we can call on_resize
        super( RatioViewport, self ).__init__(
            window,
            [ [0, 0], [1, 1] ]
            )

        self._ratio = numpy.array(
            ratio,
            dtype = numpy.float
            )
        if self.ratio.shape != (2,2):
            raise ValueError(
                "Viewport ratio must be an array with shape (2,2)"
                )

        # work out the actual rect size
        self.on_resize( window.width, window.height )

    def on_resize( self, width, height ):
        """Event handler to be called when the window
        is resized.

        Args:
            width (int): The width, in pixels, of the window's
            renderable area.
            height (int): The height, in pixels, of the window's
            renderable area.
        """
        # update our pixel size
        # find our window's dimensions
        window_rect = pygly.window.create_rectangle( self.window )

        # calculate our viewport size
        rect = window_rect.view( dtype = numpy.float ) * self.ratio
        self.rect = rect.view( dtype = numpy.int )

    @property
    def ratio( self ):
        """The viewport's ratio.

        .. note::
            This is an @property decorated method which allows
            retrieval and assignment of the scale value.
        """
        return self._ratio

    @ratio.setter
    def ratio( setter, rect ):
        # update our ratio
        self._ratio[:] = rect

        # update our rectangle
        self.on_resize( self.window.width, self.window.height )

