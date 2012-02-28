'''
Created on 20/06/2011

@author: adam
'''

from pyglet.gl import *

from scene_node import SceneNode


class RenderNode( SceneNode ):
    render_debug_cube = False
    
    
    def __init__( self, name ):
        super( RenderNode, self ).__init__( name )
    
