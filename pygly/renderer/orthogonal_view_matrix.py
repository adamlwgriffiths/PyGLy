'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *
import numpy

from view_matrix import ViewMatrix
from pygly.maths import rectangle


class OrthogonalViewMatrix( ViewMatrix ):


    def __init__(
        self,
        scale,
        near_clip = 1.0,
        far_clip = 100.0
        ):
        """
        Initialises an Orthographic (2D) view matrix.

        @param scale: The scale to apply to the width and
        height of the orthogonal view.
        The dimensions of the view matrix (left, right, bottom, top)
        are calculated as follows:
        height = 1.0 * scale.y
        width = 1.0 * scale.z * viewport aspect ratio 
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
        height = self.scale[ 1 ]
        width = self.scale[ 0 ] * viewport.aspect_ratio( window )
        half_width = width / 2.0
        half_height = height / 2.0
        glOrtho(
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

