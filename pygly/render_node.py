# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 19:01:19 2011

@author: adam
"""

from tree_leaf import TreeLeaf


class RenderNode( TreeLeaf ):
    
    
    def __init__( self, name ):
        super( RenderNode, self ).__init__()

        self.name = name
    
    def on_context_lost( self ):
        pass
    
    def render( self ):
        pass
        
