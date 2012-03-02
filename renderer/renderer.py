'''
Created on 20/06/2011

@author: adam
'''

from pyglet.gl import *

from window import Window
from viewport import Viewport
from scene.scene_node import SceneNode


class Renderer( object ):
    
    
    def __init__( self ):
        super( Renderer, self ).__init__()
        
        self.root = SceneNode( '/root' )
        self.windows = set([])
        
        # over-ride the default event loop
        pyglet.app.EventLoop.idle = self.idle
        
        # ensure we're using counter-clockwise winding
        glFrontFace( GL_CCW )

    def add_window( self, window ):
        # register to handle window events
        # we can't over-ride the on_resize method of window or OGL will
        # stop rendering
        window.push_handlers( self )

        # add to our list of windows
        self.windows.add( window )

    def remove_window( self, window ):
        # stop listening to events
        window.remove_handlers( self )

        # remove the window from our list
        self.windows.remove( window )
    
    def idle( self ):
        # we need to over-ride the default idle logic
        # by default, pyglet calls on_draw after EVERY batch of events
        # which without hooking into, causes ghosting
        # and if we do hook into it, it means we render after every event
        # which is REALLY REALLY BAD
        pyglet.clock.tick( poll = True )
        # don't call on_draw
        return pyglet.clock.get_sleep_time( sleep_idle = True )
    
    def on_context_lost( self ):
        """
        Pyglet event handler method.
        """
        print "on_context_lost"

        # update our render nodes
        self.root.on_context_lost()
    
    def render( self ):
        # iterate through our windows
        for window in self.windows:
            # render each window
            window.render()
    
    def flip( self ):
        for window in self.windows:
            window.flip()
    
