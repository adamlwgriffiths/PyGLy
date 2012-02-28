'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *

import maths.quaternion
import maths.matrix44

from scene_node import SceneNode
import debug_cube


class CameraNode( SceneNode ):
    render_debug_cube = False
    
    
    def __init__( self, name, fov = 60.0, near_clip = 1.0, far_clip = 100.0 ):
        super( CameraNode, self ).__init__( name )
        
        self.fov = fov
        self.near_clip = near_clip
        self.far_clip = far_clip
    
    def apply_projection_matrix( self, window_width, window_height ):
        # http://www.songho.ca/opengl/gl_transform.html
        tangent = math.radians( self.fov )
        
        # tangent of half fovY
        aspect_ratio = float(window_width) / float(window_height)
        
        # half height of near plane
        height = self.near_clip * tangent
        
        # half width of near plane
        width = height * aspect_ratio
        
        glFrustum( -width, width, -height, height, self.near_clip, self.far_clip )
    
    def apply_model_view( self ):
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
    
