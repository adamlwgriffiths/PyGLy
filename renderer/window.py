'''
Created on 02/03/2012

@author: adam
'''

import heapq

from pyglet.gl import *

from viewport import Viewport


class Window( object ):
    
    
    def __init__( self, renderer, window ):
        super( Window, self ).__init__()

        if renderer is None:
            raise ValueError( 'Window received a null renderer' )
        if window is None:
            raise ValueError( 'Window received a null window object' )
        
        self.renderer = renderer
        self.window = window
        self.viewports = []
        
        # register to handle window events
        # we can't over-ride the on_resize method of window or OGL will
        # stop rendering
        window.push_handlers( self )

    def push_handlers( self, *args, **kwargs ):
        self.window.push_handlers( *args, **kwargs )

    def remove_handlers( self, *args, **kwargs ):
        self.window.remove_handlers( *args, **kwargs )

    @property
    def width( self ):
        return self.window.width

    @property
    def height( self ):
        return self.window.height

    def close( self ):
        return self.window.close()

    def _add_viewport( self, viewport, z_value ):
        # add to the viewport list
        self.viewports.append(
            (z_value, viewport)
            )

        # re-sort the viewports
        self.viewports.sort(
            key = lambda viewport_tuple: viewport_tuple[ 0 ]
            )

        # tell the viewport how big the window is
        #viewport.set_window_size(
        #    self.window.width, self.window.height
        #    )

    def _remove_viewport( self, viewport ):
        self.viewports = [ current_viewport for current_viewport in self.viewports if current_viewport[ 1 ] != viewport ]
    
    def on_resize( self, width, height ):
        """
        Pyglet event handler method.
        """
        # update our viewports
        #for viewport in self.viewports:
        #    viewport.set_window_size( width, height )
    
    def on_context_lost( self ):
        """
        Pyglet event handler method.
        """
        # notify the viewport of our window
        # size in-case it changed
        for viewport in self.viewports:
            viewport.set_window_size(
                self.window.width,
                self.window.height
                )

    def on_close( self ):
        # TODO: remove ourself from the renderer?
        pass

    def render( self ):
        # set ourself as the active window
        self.window.switch_to()

        # clear the screen
        glClear( GL_COLOR_BUFFER_BIT )

        for viewport_tuple in self.viewports:
            glClear( GL_DEPTH_BUFFER_BIT )
            viewport = viewport_tuple[ 1 ]
            # set the viewport as active
            viewport.set_active()

            # clear the viewports contents
            viewport.clear()
            
            # set the viewport up for rendering
            viewport.setup_for_3d()
            
            # process the scene graph
            self.renderer.root.render()
    
    def flip( self ):
        self.window.flip()
    
