'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *

from Pyrr import Quaternion
from Pyrr import Matrix44

from SceneNode import SceneNode


class CameraNode( SceneNode ):
    renderDebugCube = False
    
    
    def __init__( self, name, fov = 60.0, nearClip = 1.0, farClip = 100.0 ):
        super( CameraNode, self ).__init__( name )
        
        self.fov = fov
        self.nearClip = nearClip
        self.farClip = farClip
    
    def applyProjectionMatrix( self, windowWidth, windowHeight ):
        # http://www.songho.ca/opengl/gl_transform.html
        tangent = math.radians( self.fov )
        
        # tangent of half fovY
        aspectRatio = float(windowWidth) / float(windowHeight)
        
        # half height of near plane
        height = self.nearClip * tangent
        
        # half width of near plane
        width = height * aspectRatio
        
        glFrustum( -width, width, -height, height, self.nearClip, self.farClip )
    
    def applyModelView( self ):
        # convert our quaternion to a matrix
        #matrix = Matrix44.fromInertialToObjectQuaternion( self.orientation )
        matrix = Matrix44.fromInertialToObjectQuaternion( self.worldOrientation )
        
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
        worldTranslation = self.worldTranslation
        glTranslatef(
            -worldTranslation[ 0 ],
            -worldTranslation[ 1 ],
            -worldTranslation[ 2 ]
            )
    
    def render( self ):
        # apply our transforms
        glPushMatrix()
        
        self.applyTranslations()
        
        if self.renderDebugCube == True:
            DebugCube.renderDebugCube()
        
        # continue on to our children
        for child in self.children:
            child.render()
        
        # undo our transforms
        glPopMatrix()
    


