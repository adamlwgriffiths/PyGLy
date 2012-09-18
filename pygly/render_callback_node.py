"""
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
"""

from render_node import RenderNode


class RenderCallbackNode( RenderNode ):
    """A RenderNode that takes an initialisation and a
    render function as callbacks to perform rendering.
    """
    
    
    def __init__( self, name, initialise_callback, render_callback ):
        """Initialises the node with the specified callbacks.

        Args:
            name: The name to give the node.
            initialise_callback: The function to call when the
            node is to be initialised.
            The function must accept a pointer to this object.
            render_callback: The function to call when the
            node is to be rendered.
            The function must accept a pointer to this object.
            It must also accept a **kwargs parameter which will
            be passed from the render() method.
        Raises:
            ValueError: Raised if the render callback == None.
        """
        super( RenderCallbackNode, self ).__init__( name )

        if render_callback == None:
            raise ValueError(
                "RenderNode render_callback cannot be None"
                )
        
        self.initialise_callback = initialise_callback
        self.render_callback = render_callback
        
        # initialise the mesh now
        if self.initialise_callback != None:
            self.initialise_callback( self )
    
    def on_context_lost( self ):
        # re-create any data for the mesh
        if self.initialise_callback != None:
            self.initialise_callback( self )
    
    def render( self, **kwargs ):
        self.render_callback( self, **kwargs )
        
