'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *

from view_matrix import ViewMatrix


class OrthogonalViewMatrix( ViewMatrix ):


    def __init__(
        self,
        near_clip = 1.0,
        far_clip = 100.0
        ):
        super( OrthogonalViewMatrix, self ).__init__()

        if far_clip <= near_clip:
            raise ValueError( "Far clip cannot be less than near clip" )

        self.near_clip = near_clip
        self.far_clip = far_clip

    def push_view_matrix( self, viewport ):
        # setup our projection matrix
        glMatrixMode( GL_PROJECTION )
        glPushMatrix()
        glLoadIdentity()

        # set the ortho matrix to be from
        # 0 -> width and 0 -> height
        # with near clip of -1 and far clip
        # of +1
        # http://stackoverflow.com/questions/4269079/mixing-2d-and-3d-in-opengl-using-pyglet
        glOrtho(
            0, viewport.width,
            0, viewport.height,
            -1.0, 1.0
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
            dtype = numpy.float32
            )

