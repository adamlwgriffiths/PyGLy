'''
Created on 23/03/2012

@author: adam

TODO: the viewport will need to handle cocos
translations of the layer itself
'''

from cocos.layer.base_layers import Layer as CocosLayer
from cocos.director import director
from pyglet.gl import *

from renderer.viewport import Viewport
import renderer.window as window


class Layer( CocosLayer ):

    def __init__( self ):
        super( CocosLayer, self ).__init__()

        # initialise our variables
        self.pygly_scene_node = None
        self.pygly_camera = None

        # create a default viewport that
        # stretches the entire screen
        self.pygly_viewport = Viewport(
            [ 0.0, 0.0, 1.0, 1.0 ]
            )

    def transform( self ):
        """
        Apply the model view transform for the camera
        """
        self.pygly_viewport.push_model_view()

    def draw(self, *args, **kwargs):
        """
        Draws a PyGLy scene as a Cocos2D layer
        """
        super( CocosLayer, self ).draw( *args, **kwargs )

        # enable depth testing
        director.set_depth_test( True )

        window.render(
            director.window,
            [ self.pygly_viewport ]
            )

