'''
Created on 02/03/2012

@author: adam
'''

import heapq

from pyglet.gl import *

from viewport import Viewport
from scene.scene_node import SceneNode


class Window( object ):

    
    def __init__( self, window ):
        super( Window, self ).__init__()

        if window is None:
            raise ValueError( 'Window received a null window object' )
        
        self.window = window
        
        # register to handle window events
        # we can't over-ride the on_resize method of window or OGL will
        # stop rendering
        window.push_handlers( self )

    def push_handlers( self, *args, **kwargs ):
        self.window.push_handlers( *args, **kwargs )

    def remove_handlers( self, *args, **kwargs ):
        self.window.remove_handlers( *args, **kwargs )

    def close( self ):
        return self.window.close()

    def on_resize( self, width, height ):
        """
        Pyglet event handler method.
        """
        pass
    
    def on_context_lost( self ):
        """
        Pyglet event handler method.
        """
        # notify the scene graph
        scene_node.root.on_context_lost()

    def on_close( self ):
        pass

    def set_active( self ):
        self.window.switch_to()

    def clear( self, values = GL_COLOR_BUFFER_BIT ):
        self.set_active()
        glClear( values )

    def render( self, viewports ):
        # set ourself as the active window
        self.set_active()

        # clear the screen
        self.clear( values = GL_COLOR_BUFFER_BIT )

        for viewport in viewports:
            viewport.set_active( self.window )
            viewport.clear(
                self.window,
                values = GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT
                )
            viewport.apply_view_matrix( self.window )
            viewport.setup_viewport()
            viewport.render( self.window )
            viewport.tear_down_viewport()
    
    def flip( self ):
        self.window.flip()
    
