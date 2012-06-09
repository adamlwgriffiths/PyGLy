'''
Created on 20/06/2011

@author: adam
'''

import numpy

import pygly.window
from viewport import Viewport


class RatioViewport( Viewport ):
    
    
    def __init__( self, window, ratio ):
        """
        Creates a viewport with the size of rect.

        @param rect: An array with the shape (2,2).
        Values are in percentages (0.0 -> 1.0).
        Values may exceed the window size but will be off the screen.
        OpenGL may place limits on how far off screen a viewport
        may go.
        """

        # we need self._rect to be valid
        # before we can call on_resize
        super( RatioViewport, self ).__init__(
            window,
            [ [0, 0], [1, 1] ]
            )

        self.ratio = numpy.array(
            ratio,
            dtype = numpy.int
            )
        if self.ratio.shape != (2,2):
            raise ValueError(
                "Viewport ratio must be an array with shape (2,2)"
                )

        # work out the actual rect size
        self.window = window
        self.on_resize( window.width, window.height )

    def on_resize( self, width, height ):
        # update our pixel size
        window_rect = pygly.window.create_rectangle( self.window )
        self.rect = window_rect * self.ratio

