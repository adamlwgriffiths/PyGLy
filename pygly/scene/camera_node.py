'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *

import pygly.maths.quaternion
import pygly.maths.matrix44

from pygly.renderer.view_matrix import ViewMatrix
from scene_node import SceneNode
import debug_axis


class CameraNode( SceneNode ):
    render_debug_cube = False
    
    
    def __init__( self, name, view_matrix ):
        super( CameraNode, self ).__init__( name )
        
        self.view_matrix = view_matrix
    
    def push_model_view( self ):
        # setup our model view matrix
        glMatrixMode( GL_MODELVIEW )
        glPushMatrix()
        glLoadIdentity()

        # convert our quaternion to a matrix
        matrix = pygly.maths.matrix44.from_inertial_to_object_quaternion( self.world_orientation )

        # we need to apply the inverse of the matrix
        # we do this by simply transposing the matrix
        matrix = matrix.T

        # convert to ctype for OpenGL
        # http://groups.google.com/group/pyglet-users/browse_thread/thread/a2374f3b51263bc0
        glMatrix = (GLfloat * matrix.size)(*matrix.flat)
        glMultMatrixf( glMatrix )
        
        # add our translation to the matrix
        # translate the scene in the opposite direction
        # we have to do this after the orientation
        # use the world translation incase we're attached to something
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
        
        # check if we should render some debug info
        if SceneNode.debug == True:
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

    def viewport_point_to_ray( self, point ):
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
        local_ray = self.view_matrix.point_to_ray( point )

        # convert our quaternion to a matrix
        matrix = pygly.maths.matrix44.from_inertial_to_object_quaternion(
            self.world_orientation
            )
        pygly.maths.matrix44.scale( matrix, self.scale, matrix )
        pygly.maths.matrix44.set_translation( matrix,
            self.world_translation,
            out = matrix
            )
        pygly.maths.matrix44.inertial_to_object( local_ray[ 0 ], matrix )
        pygly.maths.matrix44.inertial_to_object( local_ray[ 1 ], matrix )
        return local_ray
    

