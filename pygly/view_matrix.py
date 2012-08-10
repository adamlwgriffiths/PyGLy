'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

import weakref

from pyglet.gl import *


class ViewMatrix( object ):
    """Base class for View Matrix objects.

    Handles a number of common functions.
    """


    def __init__( self, aspect_ratio, near_clip, far_clip ):
        """Creates a view matrix object.

        Args:
            aspect_ratio: The aspect ratio of the viewport.
            This can be updated at any time.
            near_clip: The nearest distance to render objects.
            far_clip: The furthest distance to render objects.
        Raises:
            ValueError: Raised if the far clip is <= the near clip.
        """
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

    def __enter__( self ):
        self.push_view_matrix()

    def __exit__( self, type, value, traceback ):
        self.pop_view_matrix()

    @property
    def matrix( self ):
        """The current view matrix.
        """
        if self.dirty == True:
            self._update()

        return self._matrix

    def on_change_aspect_ratio( self, aspect_ratio ):
        """Updates the aspect ratio.

        Used to hook into Viewport events.

        Args:
            aspect_ratio: The new aspect ratio to set.
        """
        self.aspect_ratio = aspect_ratio

    def push_view_matrix( self ):
        """Pushes the frustrum matrix onto the projection
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
        """Pops the current viewport off the matrix stack.
        """
        glMatrixMode( GL_PROJECTION )
        glPopMatrix()

    def _update( self ):
        """Updates the matrix and sets the dirty flag to False
        """
        # implement this
        raise NotImplementedError()

    @property
    def aspect_ratio( self ):
        """The aspect ratio.

        This is an @property decorated method which allows
        retrieval and assignment of the scale value.
        """
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
        """The near clip value.

        This is an @property decorated method which allows
        retrieval and assignment of the scale value.
        """
        return self._near_clip

    @near_clip.setter
    def near_clip( self, near_clip ):
        if self._near_clip == near_clip:
            return
        self._near_clip = near_clip
        self.dirty = True

    @property
    def far_clip( self ):
        """The far clip value.

        This is an @property decorated method which allows
        retrieval and assignment of the scale value.
        """
        return self._far_clip

    @far_clip.setter
    def far_clip( self, far_clip ):
        if self._far_clip == far_clip:
            return
        self._far_clip = far_clip
        self.dirty = True

    def create_ray_from_ratio_point( self, point ):
        """Returns a local ray cast from the camera co-ordinates
        at 'point'.

        The ray will begin at the near clip plane.
        The ray is relative to the origin.
        The ray will project from the near clip plane
        down the -Z plane toward the far clip plane.

        The ray is in intertial space and must be transformed
        to the objects intended translation and orientation.

        Args:
            point: The 2D point, relative to this view matrix,
            to project a ray from. A list of 2 float values.
            [0.0, 0.0] is the Bottom Left.
            [viewport.width, viewport.height] is the Top Right.
        Returns:
            A ray consisting of 2 vectors (shape = 2,3).
        """
        raise NotImplementedError()

