'''
Created on 03/02/2012

@author: adam
'''

from pyglet.gl import *

from scene_node import SceneNode
import debug_cube

    
class Scene( object ):
    """
    Defines a scene to be rendered.
    """
    
    
    def __init__( self, name ):
        super( Scene, self ).__init__()
        
        self.name = name
        self.node = SceneNode( '/root' )

    def render( self ):
        # continue on to our children
        self.node.render()


if __name__ == "__main__":
    pass

