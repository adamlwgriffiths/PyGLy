'''
Created on 20/06/2011

@author: adam
'''

import weakref

import numpy
from pyglet.gl import *

import pygly.renderer.window
import pygly.maths.rectangle


class Viewport( object ):
    
    
    def __init__( self, rect ):
        """
        Creates a viewport with the size of rect.

        @param rect: An array with the shape (2,2).
        Values are from 0.0 -> 1.0.
        Values may exceed this but will be off the screen.
        A rect of [ [0.0,0.0],[1.0,1.0] ] is the equivalent
        of a whole window.
        """
        super( Viewport, self ).__init__()

        self.camera = None
        self.scene_node = None
        self.viewport_ratio = numpy.array(
            rect,
            dtype = numpy.float
            )

        if self.viewport_ratio.shape != (2,2):
            raise ValueError(
                "Viewport rect must be an array with shape (2,2)"
                )

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
    
    def switch_to( self, window ):
        """
        Calls glViewport which sets up the viewport
        for rendering.

        To reset this call
        pygly.renderer.window.set_viewport_to_window.

        This is essentially a wrapper around calling
        pygly.renderer.window.set_viewport_to_rect with the
        viewport.pixel_rect as the parameter.
        """
        # update our viewport size
        pixels = self.pixel_rect( window )
        pygly.renderer.window.set_viewport_to_rect( pixels )

    def aspect_ratio( self, window ):
        """
        Returns the aspect ratio of the viewport.

        Aspect ratio is the ratio of width to height
        a value of 2.0 means width is 2*height
        """
        pixels = self.pixel_rect( window )
        aspect_ratio = float(pixels[ (1,0) ]) / float(pixels[ (1,1) ])
        return aspect_ratio

    def scissor_to_viewport( self, window ):
        """
        Calls glScissor with the size of the viewport.

        It is up to the user to call
        glEnable(GL_SCISSOR_TEST).

        To undo this, use renderer.window.scissor_to_window

        This is essentially a wrapper around calling
        pygly.renderer.window.scissor_to_rect with the
        viewport.pixel_rect as the parameter.
        """
        rect = self.pixel_rect( window )
        pygly.renderer.window.scissor_to_rect( rect )

    def clear(
        self,
        window,
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
        self.scissor_to_viewport( window )

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
        @param point: The 2D point, relative to this viewport
        to project a ray from. The valid range for the point
        values is from 0.0 <= x <= 1.0.
        @return A ray consisting of 2 vectors (shape = 2,3).
        The ray will begin at the near clip plane.
        If the viewport has no camera, None will be returned.
        """
        # check that the point resides within the viewport
        if \
            point[ 0 ] < 0.0 or \
            point[ 0 ] > 1.0 or \
            point[ 1 ] < 0.0 or \
            point[ 1 ] > 1.0:
            raise ValueError( "Point is not within viewport" )

        # tell our camera to cast the ray
        if self.camera == None:
            # no camera
            return None

        return self.camera().viewport_point_to_ray( point )

    def is_window_point_within_viewport( self, window, point ):
        """
        Checks if a point relative to the window is
        within the viewport.
        """
        pixel_rect = self.pixel_rect( window )
        return pygly.maths.rectangle.is_point_within_rect(
            point,
            pixel_rect
            )

    def pixel_rect( self, window ):
        """
        Returns the size in pixels of the viewport.
        """
        return pygly.maths.rectangle.scale_by_vector(
            self.viewport_ratio,
            [ window.width, window.height ]
            )

    @property
    def ratio_x( self ):
        return self.viewport_ratio[ (0,0) ]

    @property
    def ratio_y( self ):
        return self.viewport_ratio[ (0,1) ]
    
    @property
    def ratio_width( self ):
        return self.viewport_ratio[ (1,0) ]
    
    @property
    def ratio_height( self ):
        return self.viewport_ratio[ (1,1) ]


if __name__ == '__main__':
    window = pyglet.window.Window(
        fullscreen = False,
        width = 1024,
        height = 512
        )
    viewport = Viewport( [[0.0, 0.0], [1.0, 1.0]] )
    assert viewport.ratio_x == 0.0
    assert viewport.ratio_y == 0.0
    assert viewport.ratio_width == 1.0
    assert viewport.ratio_height == 1.0

    assert viewport.aspect_ratio( window ) == 2.0

    pixel_rect = viewport.pixel_rect( window )
    assert pixel_rect[ (0,0) ] == 0
    assert pixel_rect[ (0,1) ] == 0
    assert pixel_rect[ (1,0) ] == 1024
    assert pixel_rect[ (1,1) ] == 512

