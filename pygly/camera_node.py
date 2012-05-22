'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *

from pyrr import quaternion
from pyrr import matrix44

from view_matrix import ViewMatrix
from scene_node import SceneNode
import debug_axis


class CameraNode( SceneNode ):
    
    
    def __init__( self, name, view_matrix ):
        super( CameraNode, self ).__init__( name )
        
        self.view_matrix = view_matrix
    
    def push_model_view( self ):
        # setup our model view matrix
        glMatrixMode( GL_MODELVIEW )
        glPushMatrix()
        glLoadIdentity()

        # convert our quaternion to a matrix
        matrix = matrix44.create_from_quaternion(
            self.world_orientation
            )

        # we need to apply the transpose of the matrix
        matrix = matrix.T

        # convert to ctype for OpenGL
        # http://groups.google.com/group/pyglet-users/browse_thread/thread/a2374f3b51263bc0
        glMatrix = (GLfloat * matrix.size)(*matrix.flat)
        glMultMatrixf( glMatrix )
        
        # add our translation to the matrix
        # translate the scene in the opposite direction
        # we have to do this after the orientation
        # use the world translation incase we're attached
        # to something
        world_translation = self.world_translation
        glTranslatef(
            -world_translation[ 0 ],
            -world_translation[ 1 ],
            -world_translation[ 2 ]
            )

    def pop_model_view( self ):
        glMatrixMode( GL_MODELVIEW )
        glPopMatrix()
    
    def render( self ):
        # apply our transforms
        glPushMatrix()
        self.apply_translations()
        
        # render some debug info
        self.render_debug_info()
        
        # continue on to our children
        for child in self.children:
            child.render()
        
        # undo our transforms
        glPopMatrix()

    def render_debug_info( self ):
        """
        Renders debug information at the current
        gl translation.
        The camera doesn't want to blind itself
        with a cube, so we don't render that.
        """
        debug_axis.render()

    def create_ray_from_viewport_point( self, point ):
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
        """
        # convert the point to a ray
        # the ray is in the format
        # [ [near.x,near.y,near.z], [far.x,far.y,far.z] ]
        local_ray = self.view_matrix.create_ray_from_viewport_point( point )

        # convert our quaternion to a matrix
        matrix = matrix44.create_from_quaternion(
            self.world_orientation
            )
        matrix44.scale( matrix, self.scale, matrix )
        matrix44.set_translation(
            matrix,
            self.world_translation,
            out = matrix
            )
        matrix44.apply_to_vector( local_ray[ 0 ], matrix )
        matrix44.apply_to_vector( local_ray[ 1 ], matrix )
        return local_ray
    

