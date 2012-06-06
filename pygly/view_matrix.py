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
            raise ValueError(
                "Far clip cannot be less than near clip"
                )

        self._near_clip = near_clip
        self._far_clip = far_clip
        self._aspect_ratio = aspect_ratio

        self._matrix = None
        self.dirty = True

    @property
    def matrix( self ):
        if self.dirty == True:
            self._update()

        return self._matrix

    def on_change_aspect_ratio( self, aspect_ratio ):
        """
        Updates the aspect ratio.

        Used to hook into Viewport events.
        """
        self.aspect_ratio = aspect_ratio

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

        glLoadMatrixf(
            (GLfloat * self.matrix.size)(*self.matrix.flat)
            )

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

    @property
    def aspect_ratio( self ):
        return self._aspect_ratio

    @aspect_ratio.setter
    def aspect_ratio( self, aspect_ratio ):
        # don't continue if the value hasn't changed
        if self._aspect_ratio == aspect_ratio:
            return
        self._aspect_ratio = aspect_ratio
        self.dirty = True

    @property
    def near_clip( self ):
        return self._near_clip

    @near_clip.setter
    def near_clip( self, near_clip ):
        if self._near_clip == near_clip:
            return
        self._near_clip = near_clip
        self.dirty = True

    @property
    def far_clip( self ):
        return self._far_clip

    @far_clip.setter
    def far_clip( self, far_clip ):
        if self._far_clip == far_clip:
            return
        self._far_clip = far_clip
        self.dirty = True

    def create_ray_from_ratio_point( self, point ):
        raise NotImplementedError()

