'''
Created on 20/06/2011

@author: adam
'''

import math

import numpy
from pyglet.gl import *

from view_matrix import ViewMatrix
import maths.vector


class ProjectionViewMatrix( ViewMatrix ):


    def __init__(
        self,
        fov = 60.0,
        near_clip = 1.0,
        far_clip = 100.0
        ):
        super( ProjectionViewMatrix, self ).__init__()

        if far_clip <= near_clip:
            raise ValueError( "Far clip cannot be less than near clip" )

        self.fov = fov
        self.near_clip = near_clip
        self.far_clip = far_clip

    @staticmethod
    def calculate_plane_size( window, viewport, fov, distance ):
        # http://www.songho.ca/opengl/gl_transform.html
        # http://nehe.gamedev.net/article/replacement_for_gluperspective/21002/
        # http://steinsoft.net/index.php?site=Programming/Code%20Snippets/OpenGL/gluperspective&printable=1
        aspect_ratio = viewport.aspect_ratio( window )
        tangent = math.radians( fov )
        height = distance * tangent
        width = height * aspect_ratio

        return width * 2.0, height * 2.0

    def calculate_near_clip_plane_size( self, window, viewport ):
        return self.calculate_plane_size(
            window,
            viewport,
            self.fov,
            self.near_clip
            )

    def calculate_far_clip_plane_size( self, window, viewport ):
        return self.calculate_plane_size(
            window,
            viewport,
            self.fov,
            self.far_clip
            )

    def push_view_matrix( self, window, viewport ):
        # setup our projection matrix
        glMatrixMode( GL_PROJECTION )
        glPushMatrix()
        glLoadIdentity()

        # calculate the near plane's size
        width, height = self.calculate_near_clip_plane_size(
            window,
            viewport
            )
        width /= 2.0
        height /= 2.0

        glFrustum(
            -width, width,
            -height, height,
            self.near_clip, self.far_clip
            )
    
    def pop_view_matrix( self ):
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()

    def calculate_point_on_plane( self, window, viewport, point, distance ):
        # calculate the near plane's size
        width, height = self.calculate_plane_size(
            window,
            viewport,
            self.fov,
            distance
            )

        # convert the point from a viewport point
        # to a near plane point
        viewport_size = viewport.dimension_in_pixels( window )
        scale = [ width / viewport_size[ 2 ], height / viewport_size[ 3 ] ]

        plane_point = numpy.array( point, dtype = numpy.float )
        # scale the point from viewport coordinates to plane coordinates
        plane_point *= scale

        # 0,0 is bottom left, we need to make this the centre
        plane_point[ 0 ] -= width / 2.0
        plane_point[ 1 ] -= height / 2.0

        return plane_point

    def point_to_ray( self, window, viewport, point ):
        """
        Returns a local ray cast from the camera co-ordinates
        at 'point'.

        The ray is in intertial space and must be transformed
        to the objects intended translation and orientation.

        @param window: The window the viewport resides on.
        @param viewport: The viewport used for picking.
        @param point: The 2D point, relative to this view matrix,
        to project a ray from. A list of 2 float values.
        [0.0, 0.0] is the Bottom Left.
        [viewport.width, viewport.height] is the Top Right.
        @returns A ray consisting of 2 vectors (shape = 2,3).
        The vector will extend from Z = near_clip -> near_clip - 1.0
        """
        # calculate the point on the near plane
        near_plane_point = self.calculate_point_on_plane(
            window,
            viewport,
            point,
            self.near_clip
            )
        far_plane_point = self.calculate_point_on_plane(
            window,
            viewport,
            point,
            self.far_clip
            )

        # this point is immediately mappable
        # to a vector from 0,0,0 to
        # point.x, point.y, -near_clip
        near_vec = numpy.array(
            [
                near_plane_point[ 0 ],
                near_plane_point[ 1 ],
                -self.near_clip
                ],
            dtype = numpy.float
            )
        far_vec = numpy.array(
            [
                far_plane_point[ 0 ],
                far_plane_point[ 1 ],
                -self.far_clip
                ],
            dtype = numpy.float
            )

        # convert the 2 vectors into a ray from
        # near_vec to far_vec
        return numpy.array(
            [
                near_vec,
                far_vec
                ],
            dtype = numpy.float
            )

