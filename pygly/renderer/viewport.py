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
        self.scene = None
        self.dimensions = (
            rect[ 0 ],
            rect[ 1 ],
            rect[ 2 ],
            rect[ 3 ]
            )

    def set_camera( self, scene, camera ):
        self.scene = scene
        self.camera = weakref.ref( camera )
    
    def switch_to( self, window ):
        # update our viewport size
        glViewport(
            int( self.x * window.width ),
            int( self.y * window.height ),
            int( self.width * window.width ),
            int( self.height * window.height )
            )

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
    
    def apply_view_matrix( self, window ):
        # the camera is a weak pointer
        # so we need to get a reference to it
        if self.camera != None:
            camera = self.camera()
        
            # setup our projection matrix
            camera.view_matrix.apply_view_matrix( self )
        
            # apply the camera's model view
            camera.apply_model_view()

    def render( self, window ):
        # render the current scene
        if self.scene != None:
            self.scene.render()

    def setup_viewport( self ):
        """
        Over-ride this method to customise
        the opengl settings for this viewport
        """
        pass

    def tear_down_viewport( self ):
        """
        Over-ride this method to undo
        any customizations done in
        'setup_viewport'
        """
        pass

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
    

