"""
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
"""

from pyglet.gl import *

from scene_node import SceneNode


class RenderNode( SceneNode ):
    """Base class for render functionality in a Scene Graph.

    Over-ride the :meth:`~pygly.render_node.RenderNode.render_mesh`
    method to implement render functionality.
    """
    
    
    def __init__( self, name ):
        super( RenderNode, self ).__init__( name )
    
    def on_context_lost( self ):
        """Called when the graphic device context is lost.

        This method is a stub and is intended to be over-ridden.
        """
        pass
    
    def render( self, **kwargs ):
        """Called to render the mesh.

        This method is a stub and is intended to be over-ridden.
        """
        pass

