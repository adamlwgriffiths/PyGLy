'''
Created on 20/06/2011

@author: adam
'''

import weakref

import numpy
from pyglet.gl import *

# We cannot import renderer.window or we
# will get ciruclar imports
from pyrr import rectangle


class Viewport( object ):
    
    
    def __init__( self, rect ):
        """
        Creates a viewport with the size of rect.

        @param rect: An array with the shape (2,2).
        Values are in pixels
        Values may exceed the window size but will be off the screen.
        OpenGL may place limits on how far off screen a viewport
        may go.
        """
        super( Viewport, self ).__init__()

        self.camera = None
        self.scene_node = None
        self._rect = numpy.array(
            rect,
            dtype = numpy.int
            )

        if self._rect.shape != (2,2):
            raise ValueError(
                "Viewport rect must be an array with shape (2,2)"
                )

    def _get_rect( self ):
        return self._rect

    def _set_rect( self, rect ):
        if \
            self._rect[ (0, 0) ] == rect[ (0, 0) ] and \
            self._rect[ (0, 1) ] == rect[ (0, 1) ] and \
            self._rect[ (1, 0) ] == rect[ (1, 0) ] and \
            self._rect[ (1, 1) ] == rect[ (1, 1) ]:
            # no change
            return

        self._rect[:] = rect

        # notify our camera's view matrix that our
        # viewport geometry has changed
        if self.camera != None:
            self.camera().view_matrix.aspect_ratio = self.aspect_ratio

    rect = property( _get_rect, _set_rect )

    def set_camera( self, scene_node, camera ):
        """
        Set's the camera of the viewport and the
        viewport's root scene node.

        @param scene_node: The root scene_node used
        to render the viewport.
        @param camera: The camera to render the scene_node
        from.
        """
        self.scene_node = scene_node
        self.camera = weakref.ref( camera )
    
    def switch_to( self ):
        """
        Calls glViewport which sets up the viewport
        for rendering.

        To reset this call
        pygly.renderer.window.set_viewport_to_window.
        """
        # update our viewport size
        glViewport(
            int(self._rect[ (0,0) ]),
            int(self._rect[ (0,1) ]),
            int(self._rect[ (1,0) ]),
            int(self._rect[ (1,1) ])
            )

    @property
    def aspect_ratio( self ):
        """
        Returns the aspect ratio of the viewport.

        Aspect ratio is the ratio of width to height
        a value of 2.0 means width is 2*height
        """
        aspect_ratio = float(self._rect[ (1,0) ]) / float(self._rect[ (1,1) ])
        return aspect_ratio

    def scissor_to_viewport( self ):
        """
        Calls glScissor with the size of the viewport.

        It is up to the user to call
        glEnable(GL_SCISSOR_TEST).

        To undo this, use renderer.window.scissor_to_window
        """
        glScissor(
            int(self._rect[ (0,0) ]),
            int(self._rect[ (0,1) ]),
            int(self._rect[ (1,0) ]),
            int(self._rect[ (1,1) ])
            )

    def clear(
        self,
        values = GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT
        ):
        """
        Uses glScissor to perform glClear on the viewport
        only.
        """
        assert True == glIsEnabled( GL_SCISSOR_TEST )

        # clear the region
        # we use glScissor to set the pixels
        # we want to affect
        self.scissor_to_viewport()

        # clear the background or we will just draw
        # ontop of other viewports
        glClear( values )
    
    def push_view_matrix( self ):
        """
        Pushes the viewport's active camera's
        view matrix onto the stack.
        If there is no camera, no matrix is pushed.
        """
        # the camera is a weak pointer
        # so we need to get a reference to it
        if self.camera != None:
            # apply our projection matrix
            self.camera().view_matrix.push_view_matrix()

    def pop_view_matrix( self ):
        """
        Pops the viewport's active camera's
        view matrix from the stack.
        If there is no camera, no matrix is poped.
        """
        # the camera is a weak pointer
        # so we need to get a reference to it
        if self.camera != None:
            # unapply our projection matrix
            self.camera().view_matrix.pop_view_matrix()
        
    def push_model_view( self ):
        """
        Pushes the viewport's active camera's
        model matrix from the stack.
        If there is no camera, no matrix is pushed.
        """
        # the camera is a weak pointer
        # so we need to get a reference to it
        if self.camera != None:
            # apply the camera's model view
            self.camera().push_model_view()

    def pop_model_view( self ):
        """
        Pops the viewport's active camera's
        model matrix from the stack.
        If there is no camera, no matrix is poped.
        """
        # the camera is a weak pointer
        # so we need to get a reference to it
        if self.camera != None:
            # unapply the camera's model view
            self.camera().pop_model_view()

    def render( self, window ):
        """
        Triggers a render on the viewport's
        current scene node.
        It is up to the caller to ensure the
        correct window is currently active and
        the viewport has been setup.
        """
        # render the current scene
        if self.scene_node != None:
            self.scene_node.render()

    def push_viewport_attributes( self ):
        """
        Pushes the current OGL attributes
        and then calls self.setup_viewport.
        """
        glPushAttrib( GL_ALL_ATTRIB_BITS )
        self.setup_viewport()

    def pop_viewport_attributes( self ):
        """
        Pops the OGL attributes.
        Called when tearing down viewport.
        This method mirrors 'push_viewport_attributes'
        """
        glPopAttrib()

    def setup_viewport( self ):
        """
        Over-ride this method to customise
        the opengl settings for this viewport.

        The default method sets the following:
        -glEnable( GL_DEPTH_TEST )
        -glShadeModel( GL_SMOOTH )
        -glEnable( GL_RESCALE_NORMAL )
        -glEnable( GL_SCISSOR_TEST )
        """
        # enable some default options
        # use the z-buffer when drawing
        glEnable( GL_DEPTH_TEST )

        # enable smooth shading
        glShadeModel( GL_SMOOTH )

        # because we use glScale for scene graph
        # scaling, normals will get affected too.
        # GL_RESCALE_NORMAL applies the inverse
        # value of the current matrice's scale
        # this is new in OGL1.2 and SHOULD be
        # faster than glEnable( GL_NORMALIZE )
        # http://www.opengl.org/archives/resources/features/KilgardTechniques/oglpitfall/
        glEnable( GL_RESCALE_NORMAL )

        # enable GL_SCISSOR_TEST so we can selectively
        # clear areas of the window
        glEnable( GL_SCISSOR_TEST )

    def viewport_point_to_ray( self, point ):
        """
        Returns a ray cast from viewport space
        into the world.

        @param viewport: The viewport being used to cast the ray.
        @param point: The 2D point in pixels, relative to this
        viewport, to project a ray from.
        @return A ray consisting of 2 vectors (shape = 2,3).
        The ray will begin at the near clip plane.
        If the viewport has no camera, None will be returned.
        @raise ValueError: Raised if the point is < 0,0 or
        > width,height of the viewport.
        """
        # check that the point resides within the viewport
        if \
            point[ 0 ] < 0 or \
            point[ 0 ] > self.width or \
            point[ 1 ] < 0 or \
            point[ 1 ] > self.height:
            raise ValueError( "Point is not within viewport" )

        # tell our camera to cast the ray
        if self.camera == None:
            # no camera
            return None

        # convert from pixel position to relative position
        # ie, 0.0 -> 1.0
        relative_point = numpy.array(
            point,
            dtype = numpy.float
            )
        size = numpy.array(
            self._rect[ 1 ],
            dtype = numpy.float
            )
        relative_point /= size

        return self.camera().viewport_point_to_ray( relative_point )

    def is_window_point_within_viewport( self, point ):
        """
        Checks if a point relative to the window is
        within the viewport.
        """
        return rectangle.is_point_within_rect(
            point,
            self._rect
            )

    @property
    def x( self ):
        return self._rect[ (0,0) ]

    @property
    def y( self ):
        return self._rect[ (0,1) ]
    
    @property
    def width( self ):
        return self._rect[ (1,0) ]
    
    @property
    def height( self ):
        return self._rect[ (1,1) ]

    @property
    def left( self ):
        return self._rect[ (0,0) ]

    @property
    def bottom( self ):
        return self._rect[ (0,1) ]

    @property
    def right( self ):
        return self._rect[ (0,0) ] + self._rect[ (1,0) ]

    @property
    def top( self ):
        return self._rect[ (0,1) ] + self._rect[ (1,1) ]


if __name__ == '__main__':
    window = pyglet.window.Window(
        fullscreen = False,
        width = 1024,
        height = 512
        )
    viewport = Viewport(
        [
            [0, 0],
            [1024, 512]
            ]
        )
    assert viewport.x == 0
    assert viewport.y == 0
    assert viewport.width == 1024
    assert viewport.height == 512

    assert viewport.aspect_ratio == 2.0

