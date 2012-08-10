'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
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
    """A Scene Graph based camera.
    """
    
    
    def __init__( self, name, view_matrix ):
        """Creates a CameraNode object.

        Args:
            name (str): The name to give to the node.
            view_matrix: The camera's ViewMatrix.
        """
        super( CameraNode, self ).__init__( name )
        
        #: the camer's view matrix
        self.view_matrix = view_matrix

    def __enter__( self ):
        # apply our view matrix
        # and push our model view
        self.view_matrix.push_view_matrix()
        self.push_model_view()

    def __exit__( self, type, value, traceback ):
        # pop our model view
        # and our view matrix
        self.pop_model_view()
        self.view_matrix.pop_view_matrix()

    @property
    def model_view( self ):
        """Property for the camera's model view matrix.

        This is an @property decorated method.

        Returns:
            A NumPy array set to the camera's model view
            matrix.
        """
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
        """Pushes the model view matrix onto the OGL stack.

        Gets the current model view matrix and set's pushes
        it onto the OpenGL GL_MODELVIEW matrix stack.

        """
        # setup our model view matrix
        glMatrixMode( GL_MODELVIEW )
        glPushMatrix()

        # convert to ctype for OpenGL
        glLoadMatrixf(
            (GLfloat * self.model_view.size)(*self.model_view.flat)
            )

    def pop_model_view( self ):
        """Pops the model view matrix from the OGL stack.
        """
        glMatrixMode( GL_MODELVIEW )
        glPopMatrix()

    def create_ray_from_ratio_point( self, point ):
        """Returns a ray cast from 2d camera co-ordinates
        into the world.

        Args:
            window: The window the viewport resides on.
            viewport: The viewport being used to cast the ray.
            point: The 2D point, relative to this camera,
            to project a ray from. A list of 2 float values.
            [0, 0] is the Bottom Left of the viewport
            [viewport.width, viewport.height] is the Top Right of
            the viewport.
        Returns:
            A ray consisting of 2 vectors (shape = 2,3).
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

