'''
Created on 23/03/2012

@author: adam

TODO: add support for layer translation
TODO: add support for layer rotation
TODO: add support for layer scaling
To do these we need to use the current view
matrix to determine how far to move it to
get '1 pixel' accuracy as cocos works on
a pixel scale.
'''

from cocos.layer.base_layers import Layer as CocosLayer
from cocos.director import director
from pyglet.gl import *

from pygly.viewport import Viewport
import pygly.window


class Layer( CocosLayer ):
    """
    Provides a Cocos2D layer which renders a PyGLy scene.
    """

    def __init__( self ):
        super( CocosLayer, self ).__init__()

        # initialise our variables
        self.pygly_scene_node = None
        self.pygly_camera = None

        # create a default viewport that
        # stretches the entire screen
        self.pygly_viewport = Viewport(
            pygly.window.window_size_as_rect(
                director.window
                )
            )

    def transform( self ):
        """
        Apply the model view transform for the camera
        """
        self.pygly_viewport.push_model_view()

    def draw(self, *args, **kwargs):
        """
        Draws a PyGLy scene as a Cocos2D layer

        This is called by Cocos2D Director.
        """
        super( CocosLayer, self ).draw( *args, **kwargs )

        # enable depth testing
        director.set_depth_test( True )

        pygly.window.render(
            director.window,
            [ self.pygly_viewport ]
            )

