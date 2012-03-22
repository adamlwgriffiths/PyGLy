# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 19:01:19 2011

@author: adam
"""

from pyglet.gl import *

from scene_node import SceneNode
import debug_cube


class RenderCallbackNode( SceneNode ):
    
    
    def __init__( self, name, initialise_callback, render_callback ):
        super( RenderCallbackNode, self ).__init__( name )
        
        if render_callback == None:
            raise ValueError( "RenderNode render_callback cannot be None" )
        
        self.initialise_callback = initialise_callback
        self.render_callback = render_callback
        
        # initialise the mesh now
        self.initialise_callback()
    
    def on_context_lost( self ):
        # re-create any data for the mesh
        self.initialise_callback()
        
        # let our children know
        for child in self.children:
            child.on_context_lost()
    
    def render( self ):
        # apply our transforms
        glPushMatrix()
        
        self.apply_translations()
        
        if self.render_debug_cube == True:
            debug_cube.render_debug_cube()
        
        self.render_callback()
        
        # continue on to our children
        for child in self.children:
            child.render()
        
        # undo our transforms
        glPopMatrix()
    


