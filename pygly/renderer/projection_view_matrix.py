'''
Created on 20/06/2011

@author: adam
'''

import math

from pyglet.gl import *

from view_matrix import ViewMatrix


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

    def push_view_matrix( self, viewport ):
        # setup our projection matrix
        glMatrixMode( GL_PROJECTION )
        glPushMatrix()
        glLoadIdentity()

        # http://www.songho.ca/opengl/gl_transform.html
        tangent = math.radians( self.fov )

        # tangent of half fovY
        aspect_ratio = float(viewport.width) / float(viewport.height)

        # half height of near plane
        height = self.near_clip * tangent

        # half width of near plane
        width = height * aspect_ratio

        glFrustum(
            -width, width,
            -height, height,
            self.near_clip, self.far_clip
            )
    
    def pop_view_matrix( self ):
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()

