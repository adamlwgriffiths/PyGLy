'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *
import numpy

from view_matrix import ViewMatrix
from pyrr import matrix44
from pyrr import rectangle
from pyrr import ray


class OrthogonalViewMatrix( ViewMatrix ):


    def __init__(
        self,
        aspect_ratio,
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
        super( OrthogonalViewMatrix, self ).__init__(
            aspect_ratio,
            near_clip,
            far_clip
            )

        self._scale = numpy.array( scale, dtype = numpy.float )

    @property
    def scale( self ):
        return self._scale

    @scale.setter
    def scale( self, scale ):
        # check if the arrays are the same
        if numpy.array_equal(
            self._scale,
            scale
            ):
            return
        # update the scale and mark as dirty
        self._scale[:] = scale
        self.dirty = True

    def _update( self ):
        assert self.dirty == True

        left, right, bottom, top = self.bounds()
        self._matrix = matrix44.create_orthogonal_view_matrix(
            left,
            right,
            top,
            bottom,
            self.near_clip,
            self.far_clip,
            out = self._matrix
            )
        self.dirty = False

    def bounds( self ):
        """
        Returns the maximum extents of the orthographic view
        based on the current viewport and the set scale.

        @return: Returns the bounds as a tuple (left, right, bottom, top)
        """
        size = self.size()
        half_width = size[ 0 ] / 2.0
        half_height = size[ 1 ]/ 2.0
        return -half_width, half_width, -half_height, half_height

    def size( self ):
        """
        @return: Returns the size of the viewport as a vector
        """
        height = self.scale[ 1 ]
        width = self.scale[ 0 ] * self.aspect_ratio
        return numpy.array( [width, height], dtype = numpy.float )

    def create_ray_from_viewport_point( self, point ):
        """
        Returns a local ray cast from the camera co-ordinates
        at 'point'.

        The ray will begin at the near clip plane.
        The ray is relative to the origin.
        The ray will project from the near clip plane
        down the -Z plane toward the far clip plane.

        The ray is in intertial space and must be transformed
        to the objects intended translation and orientation.

        @param point: The 2D point, relative to this view matrix,
        to project a ray from. A list of 2 float values.
        [0.0, 0.0] is the Bottom Left.
        [viewport.width, viewport.height] is the Top Right.
        @returns A ray consisting of 2 vectors (shape = 2,3).
        """
        # convert the point from a viewport point
        # to a point in the ortho projection plane
        size = self.size()

        plane_point = numpy.array( point, dtype = numpy.float )
        plane_point *= size

        # 0,0 is bottom left, we need to make this the centre
        half_size = size / 2.0
        plane_point -= half_size

        line = numpy.array(
            [
                [
                    plane_point[ 0 ],
                    plane_point[ 1 ],
                    self.near_clip
                    ],
                [
                    plane_point[ 0 ],
                    plane_point[ 1 ],
                    -self.far_clip
                    ]
                ],
            dtype = numpy.float
            )
        return ray.create_from_line( line )

