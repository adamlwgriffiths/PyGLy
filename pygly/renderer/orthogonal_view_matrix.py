'''
Created on 20/06/2011

@author: adam

TODO: create a "size" calculation tool.
This would be like the controls available to
setting a desktop background.
This would receive a rectangle (the requested size)
The viewport size in pixels
And return a rectangle based on the following preferences:

Original (just use size X for the orth size)
Fit biggest (scale until the biggest dimension fits the screen)
Fit smallest (scale until the smallest dimension fits the screen)
'''

import math

from pyglet.gl import *
import numpy

from view_matrix import ViewMatrix
from pygly.maths import rectangle


class OrthogonalViewMatrix( ViewMatrix ):


    def __init__(
        self,
        near_clip = 1.0,
        far_clip = 100.0
        ):
        """
        Initialises an Orthographic (2D) view matrix.

        @param scale: The scale to applie to the matrix.
        The dimensions of the view matrix are based on the viewport
        size in order to keep the view ratio correct.
        A fullscreen viewport 
        """
        super( OrthogonalViewMatrix, self ).__init__()

        if far_clip <= near_clip:
            raise ValueError( "Far clip cannot be less than near clip" )

        self.near_clip = near_clip
        self.far_clip = far_clip
        self.scale = numpy.array( scale, dtype = numpy.float )

    def push_view_matrix( self, window, viewport ):
        # setup our projection matrix
        glMatrixMode( GL_PROJECTION )
        glPushMatrix()
        glLoadIdentity()

        # set the ortho matrix
        # http://stackoverflow.com/questions/4269079/mixing-2d-and-3d-in-opengl-using-pyglet
        half_width = viewport.ratio_width / 2.0
        half_height = viewport.ratio_height / 2.0
        glOrtho(
            self.rect
            -half_width, half_width,
            -half_height, half_height,
            self.near_clip, self.far_clip
            )

    def pop_view_matrix( self ):
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()

    def point_to_ray( self, window, viewport, point ):
        """
        Returns a local ray cast from the camera co-ordinates
        at 'point'.

        The ray is in intertial space and must be transformed
        to the objects intended translation and orientation.

        @param window: The window the viewport resides on. This is ignored.
        @param viewport: The viewport used for picking.
        @param point: The 2D point, relative to this view matrix,
        to project a ray from. A list of 2 float values.
        [0.0, 0.0] is the Bottom Left.
        [viewport.width, viewport.height] is the Top Right.
        @returns A ray consisting of 2 vectors (shape = 2,3).
        The vector will extend from Z = near_clip -> near_clip - 1.0
        """
        return numpy.array(
            [
                [ point[ 0 ], point[ 1 ], self.near_clip ],
                [ point[ 0 ], point[ 1 ],-self.far_clip ]
                ],
            dtype = numpy.float
            )

