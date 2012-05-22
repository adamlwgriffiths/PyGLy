# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 19:01:19 2011

@author: adam
"""

from scene_node import SceneNode


class RenderNode( SceneNode ):
    
    
    def __init__( self, name ):
        super( RenderNode, self ).__init__( name )
    
    def on_context_lost( self ):
        pass
    
    def render( self ):
        pass
        
