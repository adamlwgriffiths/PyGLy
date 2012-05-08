'''
Created on 20/06/2011

@author: adam
'''

import weakref

from pyglet.gl import *


class ViewMatrix( object ):


    def __init__( self, aspect_ratio, near_clip, far_clip ):
        super( ViewMatrix, self ).__init__()

        if far_clip <= near_clip:
            raise ValueError( "Far clip cannot be less than near clip" )

        self._near_clip = near_clip
        self._far_clip = far_clip
        self._aspect_ratio = aspect_ratio

        self._matrix = None
        self.dirty = True

    def push_view_matrix( self ):
        """
        Pushes the frustrum matrix onto the projection
        viewport.

        Updates the matrix if self.dirty == True
        Sets the glMatrixMode to GL_PROJECTION.
        It is up to the caller to change this after calling
        this function.
        """
        # setup our projection matrix
        glMatrixMode( GL_PROJECTION )
        glPushMatrix()
        glLoadIdentity()

        if self.dirty == True:
            self._update()

        glMatrix = (GLfloat *
        self._matrix.size)(*self._matrix.flat)
        glLoadMatrixf( glMatrix )

    def pop_view_matrix( self ):
        """
        Pops the current viewport off the matrix stack.
        """
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()

    def _update( self ):
        """
        Updates the matrix and sets the dirty flag to False
        """
        # implement this
        raise NotImplementedError()

    def _get_aspect_ratio( self ):
        return self._aspect_ratio

    def _set_aspect_ratio( self, aspect_ratio ):
        # don't continue if the value hasn't changed
        if self._aspect_ratio == aspect_ratio:
            return
        self._aspect_ratio = aspect_ratio
        self.dirty = True

    aspect_ratio = property( _get_aspect_ratio, _set_aspect_ratio )

    def _get_near_clip( self ):
        return self._near_clip

    def _set_near_clip( self, near_clip ):
        if self._near_clip == near_clip:
            return
        self._near_clip = near_clip
        self.dirty = True

    near_clip = property( _get_near_clip, _set_near_clip )


    def _get_far_clip( self ):
        return self._far_clip

    def _set_far_clip( self, far_clip ):
        if self._far_clip == far_clip:
            return
        self._far_clip = far_clip
        self.dirty = True

    far_clip = property( _get_far_clip, _set_far_clip )

