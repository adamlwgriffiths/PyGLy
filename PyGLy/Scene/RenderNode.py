'''
Created on 20/06/2011

@author: adam
'''

from pyglet.gl import *

from SceneNode import SceneNode
import DebugCube


class RenderNode( SceneNode ):
    renderDebugCube = False
    
    
    def __init__( self, name ):
        super( RenderNode, self ).__init__( name )
    
