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
    
    def render( self ):
        """Renders the scene node at it's world transform.
        
        Does the following:
            #. Pushes the SceneNode's world transform onto the GL stack.
            #. Calls render_mesh.
            #. Pops the matrix off the GL stack.
        """
        # store the existing matrix state
        glPushMatrix()

        # apply our transforms
        matrix = self.world_transform.matrix
        glMultMatrixf(
            (GLfloat * matrix.size)(*matrix.flat)
            )
        
        # render ourself
        self.render_mesh()

        # undo our transforms
        glPopMatrix()
        
    def render_mesh( self ):
        """Called to render the mesh.

        This method is a stub and is intended to be over-ridden.
        """
        pass

