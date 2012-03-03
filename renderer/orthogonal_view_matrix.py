'''
Created on 20/06/2011

@author: adam
'''

import weakref
import math

from pyglet.gl import *

class OrthogonalViewMatrix( object ):


    def __init__(
        self,
        near_clip = 1.0,
        far_clip = 100.0
        ):
        super( OrthogonalViewMatrix, self ).__init__()

        self.near_clip = near_clip
        self.far_clip = far_clip

    def apply_view_matrix( self, viewport ):
        # setup our projection matrix
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()

        # set the ortho matrix to be from
        # 0 -> width and 0 -> height
        # with near clip of -1 and far clip
        # of +1
        # http://stackoverflow.com/questions/4269079/mixing-2d-and-3d-in-opengl-using-pyglet
        glOrtho(
            0, viewport.width,
            0, viewport.height,
            -1.0, 1.0
            )

