'''
Created on 20/06/2011

@author: adam
'''

import weakref

import numpy
from pyglet.gl import *


class Viewport( object ):
    
    
    def __init__( self, rect ):
        super( Viewport, self ).__init__()

        self.camera = None
        self.dimensions = None
        self.scene_node = None
        self.dimensions = (
            rect[ 0 ],
            rect[ 1 ],
            rect[ 2 ],
            rect[ 3 ]
            )

    def set_camera( self, scene_node, camera ):
        self.scene_node = scene_node
        self.camera = weakref.ref( camera )
    
    def switch_to( self, window ):
        # update our viewport size
        glViewport(
            int( self.x_ratio * window.width ),
            int( self.y_ratio * window.height ),
            int( self.width_ratio * window.width ),
            int( self.height_ratio * window.height )
            )

    def aspect_ratio( self, window ):
        """
        Returns the aspect ratio of the viewport.

        Aspect ratio is the ratio of width to height
        a value of 2.0 means width is 2*height
        """
        size = self.size_in_pixels( window )
        aspect_ratio = float(size[ 0 ]) / float(size[ 1 ])
        return aspect_ratio

    def position_in_pixels( self, window ):
        return [
            int( self.x_ratio * window.width ),
            int( self.y_ratio * window.height )
            ]

    def size_in_pixels( self, window ):
        return [
            int( self.width_ratio * window.width ),
            int( self.height_ratio * window.height )
            ]

    def clear(
        self,
        window,
        values = GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT
        ):
        # clear the region
        # we use glScissor to set the pixels
        # we want to affect
        glEnable( GL_SCISSOR_TEST )

        position = self.position_in_pixels( window )
        size = self.size_in_pixels( window )
        glScissor( 
            position[ 0 ],
            position[ 1 ],
            size[ 0 ],
            size[ 1 ]
            )
        # clear the background or we will just draw
        # ontop of other viewports
        glClear( values )

        glDisable( GL_SCISSOR_TEST )
    
    def push_view_matrix( self, window ):
        # the camera is a weak pointer
        # so we need to get a reference to it
        if self.camera != None:
            # apply our projection matrix
            self.camera().view_matrix.push_view_matrix(
                window,
                self
                )

    def pop_view_matrix( self ):
        # the camera is a weak pointer
        # so we need to get a reference to it
        if self.camera != None:
            # unapply our projection matrix
            self.camera().view_matrix.pop_view_matrix()
        
    def push_model_view( self ):
        # the camera is a weak pointer
        # so we need to get a reference to it
        if self.camera != None:
            # apply the camera's model view
            self.camera().push_model_view()

    def pop_model_view( self ):
        # the camera is a weak pointer
        # so we need to get a reference to it
        if self.camera != None:
            # unapply the camera's model view
            self.camera().pop_model_view()

    def render( self, window ):
        # render the current scene
        if self.scene_node != None:
            self.scene_node.render()

    def push_viewport_attributes( self ):
        glPushAttrib( GL_ALL_ATTRIB_BITS )
        self.setup_viewport()

    def pop_viewport_attributes( self ):
        glPopAttrib()

    def setup_viewport( self ):
        """
        Over-ride this method to customise
        the opengl settings for this viewport.

        The default method sets the following:
        -glEnable( GL_DEPTH_TEST )
        -glShadeModel( GL_SMOOTH )
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

    def viewport_point_to_ray( self, window, point ):
        """
        Returns a ray cast from 2d window co-ordinates
        into the world.

        @param viewport: The viewport being used to cast the ray.
        @param point: The 2D point, relative to this camera,
        to project a ray from. A list of 2 float values.
        @returns A ray consisting of 2 vectors (shape = 2,3).
        """
        # check that the point resides within the viewport
        size = numpy.array(
            self.size_in_pixels( window ),
            dtype = numpy.int
            )
        if self.is_viewport_point_within_viewport(
            window,
            point
            ):
            # tell our camera to cast the ray
            if self.camera != None:
                return self.camera().point_to_ray( window, self, point )
        else:
            raise ValueError( "Point does not lie within viewport" )

        return None

    def window_point_to_ray( self, window, point ):
        """
        Returns a ray cast from 2d window co-ordinates
        into the world.
        This is the equivalent of converting the point to
        viewport co-ordinates and calling 'viewport_point_to_ray'.

        @param viewport: The window being used to cast the ray.
        @param point: The 2D point on the window to project a
        ray from. A list of 2 float values.
        @returns A ray consisting of 2 vectors (shape = 2,3).
        """
        # convert to viewport co-ordinates
        relative_point = self.window_to_viewport_point( window, point )

        return self.viewport_point_to_ray( window, relative_point )

    def window_to_viewport_point( self, window, point ):
        # convert to viewport co-ordinates
        np_point = numpy.array( point, dtype = numpy.int )
        pos = numpy.array(
            self.position_in_pixels( window ),
            dtype = numpy.int
            )
        return numpy.array( point ) - pos

    def is_viewport_point_within_viewport( self, window, point ):
        size = self.size_in_pixels( window )

        if point[ 0 ] < 0:
            return False
        elif point[ 1 ] < 0:
            return False
        elif point[ 0 ] > size[ 0 ]:
            return False
        elif point[ 1 ] > size[ 1 ]:
            return False
        return True

    def is_window_point_within_viewport( self, window, point ):
        # make the point relative to the viewport
        relative_point = numpy.array( point, type = numpy.int )
        relative_point -= self.position_in_pixels( window )
        return self.is_viewport_point_within_viewport(
            window,
            relative_point
            )

    @property
    def x_ratio( self ):
        return self.dimensions[ 0 ]

    @property
    def y_ratio( self ):
        return self.dimensions[ 1 ]
    
    @property
    def width_ratio( self ):
        return self.dimensions[ 2 ]
    
    @property
    def height_ratio( self ):
        return self.dimensions[ 3 ]


if __name__ == '__main__':
    window = pyglet.window.Window(
        fullscreen = False,
        width = 1024,
        height = 512
        )
    viewport = Viewport( [0.0, 0.0, 1.0, 1.0] )
    assert viewport.x_ratio == 0.0
    assert viewport.y_ratio == 0.0
    assert viewport.width_ratio == 1.0
    assert viewport.height_ratio == 1.0

    assert viewport.aspect_ratio( window ) == 2.0

    pixel_position = viewport.position_in_pixels( window )
    assert pixel_position[ 0 ] == 0
    assert pixel_position[ 1 ] == 0

    pixel_size = viewport.size_in_pixels( window )
    assert pixel_size[ 0 ] == 1024
    assert pixel_size[ 1 ] == 512
