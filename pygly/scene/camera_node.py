'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *

import maths.quaternion
import maths.matrix44

from renderer.view_matrix import ViewMatrix
from scene_node import SceneNode
import debug_cube


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
        #matrix = maths.matrix44.from_inertial_to_object_quaternion( self.orientation )
        matrix = maths.matrix44.from_inertial_to_object_quaternion( self.world_orientation )
        
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
        #glTranslatef( -self.translation[ 0 ], -self.translation[ 1 ], -self.translation[ 2 ] )
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
        
        if self.render_debug_cube == True:
            debug_cube.render_debug_cube()
        
        # continue on to our children
        for child in self.children:
            child.render()
        
        # undo our transforms
        glPopMatrix()
    
