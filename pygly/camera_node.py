'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *

from pyrr import quaternion
from pyrr import matrix44
from pyrr import ray

from view_matrix import ViewMatrix
from scene_node import SceneNode
import debug_axis


class CameraNode( SceneNode ):
    
    
    def __init__( self, name, view_matrix ):
        super( CameraNode, self ).__init__( name )
        
        self.view_matrix = view_matrix

    @property
    def model_view( self ):
        # convert our quaternion to a matrix
        matrix = matrix44.create_from_quaternion(
            self.world_transform.orientation
            )

        # we need to apply the transpose of the matrix
        matrix = matrix.T

        # multiply by our inverse world transform
        matrix44.multiply(
            matrix44.create_from_translation(
                -self.world_transform.translation
                ),
            matrix,
            out = matrix
            )

        return matrix
    
    def push_model_view( self ):
        # setup our model view matrix
        glMatrixMode( GL_MODELVIEW )
        glPushMatrix()

        # convert to ctype for OpenGL
        glLoadMatrixf(
            (GLfloat * self.model_view.size)(*self.model_view.flat)
            )

    def pop_model_view( self ):
        glMatrixMode( GL_MODELVIEW )
        glPopMatrix()

    def create_ray_from_ratio_point( self, point ):
        """
        Returns a ray cast from 2d camera co-ordinates
        into the world.

        @param window: The window the viewport resides on.
        @param viewport: The viewport being used to cast the ray.
        @param point: The 2D point, relative to this camera,
        to project a ray from. A list of 2 float values.
        [0, 0] is the Bottom Left of the viewport
        [viewport.width, viewport.height] is the Top Right of
        the viewport.
        @returns A ray consisting of 2 vectors (shape = 2,3).
        The first vector (result[0]) is the origin of the ray.
        The second vector (result[1]) is the direction of the ray.
        The direction is a vector of unit length.
        """
        # convert the point to a ray
        local_ray = self.view_matrix.create_ray_from_ratio_point(
            point
            )

        # convert our quaternion to a matrix
        matrix = matrix44.create_from_quaternion(
            self.world_transform.orientation
            )

        # apply our rotation to the ray direction
        matrix44.apply_to_vector( local_ray[ 1 ], matrix )

        # apply our scale
        scale_matrix = matrix44.create_from_scale(
            self.world_transform.scale
            )
        matrix44.multiply( matrix, scale_matrix )

        translate_matrix = matrix44.create_from_translation(
            self.world_transform.translation,
            )
        matrix44.multiply( matrix, translate_matrix )

        # apply the full matrix to the ray origin
        matrix44.apply_to_vector( local_ray[ 0 ], matrix )

        # make sure the ray is unit length
        ray.create_ray(
            local_ray[ 0 ],
            local_ray[ 1 ],
            out = local_ray
            )

        return local_ray

