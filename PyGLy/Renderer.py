'''
Created on 20/06/2011

@author: adam
'''

from pyglet.gl import *

from PyGLy.Scene.SceneNode import SceneNode
from Viewport import Viewport


class Renderer( object ):
    
    
    def __init__( self, window ):
        super( Renderer, self ).__init__()
        
        self.window = window
        self.root = SceneNode( '/root' )
        self.viewport = Viewport( window.width, window.height )
        
        # register to handle window events
        # we can't over-ride the on_resize method of window or OGL will
        # stop rendering
        window.push_handlers( self )
        
        # over-ride the default event loop
        pyglet.app.EventLoop.idle = self.idle
        
        # ensure we're using counter-clockwise winding
        glFrontFace( GL_CCW )
    
    def idle( self ):
        # we need to over-ride the default idle logic
        # by default, pyglet calls on_draw after EVERY batch of events
        # which without hooking into, causes ghosting
        # and if we do hook into it, it means we render after every event
        # which is REALLY REALLY BAD
        pyglet.clock.tick( poll = True )
        # don't call on_draw
        return pyglet.clock.get_sleep_time( sleep_idle = True )
    
    def on_resize( self, width, height ):
        """
        Pyglet event handler method.
        """
        # update our viewport
        self.viewport.updateViewport( width, height )
    
    def on_context_lost( self ):
        """
        Pyglet event handler method.
        """
        print "on_context_lost"
        # update our viewport
        self.viewport.updateViewport( self.window.width, self.window.height )
        
        # update our render nodes
        self.root.onContextLost()
    
    def render( self ):
        # TODO: add support for multiple viewports
        # clear screen
        # for each viewport
        #   clear buffer
        #   render
        
        # clear the screen
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        
        # set the viewport as active
        self.viewport.setActive()
        
        # set the viewport up for rendering
        self.viewport.setupFor3D()
        
        # process the scene graph
        self.root.render()
    
    def flip( self ):
        self.window.flip()
    
