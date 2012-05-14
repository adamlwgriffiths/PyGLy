# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 19:01:19 2011

@author: adam
"""

from render_node import RenderNode


class RenderCallbackNode( RenderNode ):
    
    
    def __init__( self, name, initialise_callback, render_callback ):
        super( RenderCallbackNode, self ).__init__( name )

        if render_callback == None:
            raise ValueError( "RenderNode render_callback cannot be None" )
        
        self.initialise_callback = initialise_callback
        self.render_callback = render_callback
        
        # initialise the mesh now
        if self.initialise_callback != None:
            self.initialise_callback()
    
    def on_context_lost( self ):
        # re-create any data for the mesh
        if self.initialise_callback != None:
            self.initialise_callback()
    
    def render( self ):
        self.render_callback()
        
