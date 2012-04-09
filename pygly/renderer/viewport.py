'''
Created on 20/06/2011

@author: adam
'''

import weakref

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
            int( self.x * window.width ),
            int( self.y * window.height ),
            int( self.width * window.width ),
            int( self.height * window.height )
            )

    def aspect_ratio( self, window ):
        """
        Returns the aspect ratio of the viewport.

        Aspect ratio is the ratio of width to height
        a value of 2.0 means width is 2*height
        """
        size = self.size_in_pixels( window )
        return size[ 0 ] / size[ 1 ]

    def size_in_pixels( self, window ):
        return [
            int( self.width * window.width ),
            int( self.height * window.height )
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

        glScissor( 
            int( self.x * window.width ),
            int( self.y * window.height ),
            int( self.width * window.width ),
            int( self.height * window.height )
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

    @property
    def x( self ):
        return self.dimensions[ 0 ]

    @property
    def y( self ):
        return self.dimensions[ 1 ]
    
    @property
    def width( self ):
        return self.dimensions[ 2 ]
    
    @property
    def height( self ):
        return self.dimensions[ 3 ]

    @property
    def bottom_left( self ):
        return self.x, self.y

    @property
    def top_left( self ):
        return self.x, self.y + self.height

    @property
    def bottom_right( self ):
        return self.x + self.width, self.y

    @property
    def top_right( self ):
        return self.x + self.width, self.y + self.height
    

