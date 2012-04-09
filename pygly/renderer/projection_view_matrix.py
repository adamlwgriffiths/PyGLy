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

    def _calculate_near_plane_size( self, window, viewport ):
        # http://www.songho.ca/opengl/gl_transform.html
        # http://nehe.gamedev.net/article/replacement_for_gluperspective/21002/
        # http://steinsoft.net/index.php?site=Programming/Code%20Snippets/OpenGL/gluperspective&printable=1
        aspect_ratio = viewport.aspect_ratio( window )
        tangent = math.radians( self.fov )
        height = self.near_clip * tangent
        width = height * aspect_ratio

        return width * 2.0, height * 2.0

    def push_view_matrix( self, window, viewport ):
        # setup our projection matrix
        glMatrixMode( GL_PROJECTION )
        glPushMatrix()
        glLoadIdentity()

        # calculate the near plane's size
        width, height = self._calculate_near_plane_size(
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

