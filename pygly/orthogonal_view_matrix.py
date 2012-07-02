'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

import math

from pyglet.gl import *
import numpy

from view_matrix import ViewMatrix
from pyrr import matrix44
from pyrr import rectangle
from pyrr import ray


class OrthogonalViewMatrix( ViewMatrix ):
    """Manages an orthogonal view matrix.

    Used by viewports and camera's to render a scene using
    an orthogonal perspective.
    """


    def __init__(
        self,
        aspect_ratio,
        scale,
        near_clip = 1.0,
        far_clip = 100.0
        ):
        """Initialises an orthographic (2D) view matrix.

        Args:
            aspect_ratio: The aspect ratio of the viewport.
            This can be updated at any time.
            scale: The scale to apply to the width and
            height of the orthogonal view.
            The dimensions of the view matrix (left, right, bottom, top)
            are calculated as follows:
            height = 1.0 * scale.y
            width = 1.0 * scale.z * viewport aspect ratio 
            near_clip: The nearest distance to render objects.
            far_clip: The furthest distance to render objects.
        """
        super( OrthogonalViewMatrix, self ).__init__(
            aspect_ratio,
            near_clip,
            far_clip
            )

        self._scale = numpy.array( scale, dtype = numpy.float )

    @property
    def scale( self ):
        """The scale.

        This is an @property decorated method which allows
        retrieval and assignment of the scale value.
        """
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
        """Updates the view matrix when the aspect ratio
        or scale have changed.
        """
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
        """Returns the maximum extents of the orthographic view
        based on the current viewport and the set scale.

        Returns:
            The bounds as a tuple (left, right, bottom, top)
        """
        size = self.size()
        half_width = size[ 0 ] / 2.0
        half_height = size[ 1 ]/ 2.0
        return -half_width, half_width, -half_height, half_height

    def size( self ):
        """
        Returns:
            The size of the viewport as a vector
        """
        height = self.scale[ 1 ]
        width = self.scale[ 0 ] * self.aspect_ratio

        return numpy.array(
            [ width, height ],
            dtype = numpy.float
            )

    def create_ray_from_ratio_point( self, point ):
        """Returns a local ray cast from the camera co-ordinates
        at 'point'.

        The ray will begin at the near clip plane.
        The ray is relative to the origin.
        The ray will project from the near clip plane
        down the -Z plane toward the far clip plane.

        The ray is in intertial space and must be transformed
        to the objects intended translation and orientation.

        Args:
            point: The 2D point, relative to this view matrix,
            to project a ray from. A list of 2 float values.
            [0.0, 0.0] is the Bottom Left.
            [viewport.width, viewport.height] is the Top Right.
        Returns:
            A ray consisting of 2 vectors (shape = 2,3).
        """
        # convert the point from a viewport point
        # to a point in the ortho projection plane
        size = self.size()

        plane_point = numpy.array( point, dtype = numpy.float )
        plane_point *= size

        # 0,0 is bottom left, we need to make this the centre
        half_size = size / 2.0
        plane_point -= half_size

        # convert these values to a line going from
        # -near clip to -far clip
        # this is due to the Z axis being -ve
        line = numpy.array(
            [
                [
                    plane_point[ 0 ],
                    plane_point[ 1 ],
                    -self.near_clip
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

