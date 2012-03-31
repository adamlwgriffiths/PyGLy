'''
Created on 23/03/2012

@author: adam
'''

from cocos.layer.base_layers import Layer as CocosLayer
from cocos.director import director
from pyglet.gl import *

from renderer.viewport import Viewport


class Layer( CocosLayer ):

    def __init__( self ):
        super( CocosLayer, self ).__init__()

        # initialise our variables
        self.pygly_scene_node = None
        self.pygly_camera = None

        # create a default viewport that
        # stretches the entire screen
        # TODO: this will need to handle cocos
        # translations of the layer itself
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

        # clear our depth buffer
        self.pygly_viewport.clear(
            director.window,
            values = GL_DEPTH_BUFFER_BIT
            )

        # apply our projection matrix
        # cocos only sets the view matrix up once
        # so we must store the existing view matrix
        # so we can re-apply it at the end of our render
        # store the current projection matrix
        self.pygly_viewport.push_view_matrix()

        # switch back to model view
        # and store the current matrix so
        # we can pop it off afterward
        # apply the camera transforms
        self.pygly_viewport.push_model_view()

        # setup the viewport
        self.pygly_viewport.setup_viewport()
        self.pygly_viewport.render( director.window )
        self.pygly_viewport.tear_down_viewport()

        # pop our view matrix back to the
        # original cocos matrix
        self.pygly_viewport.pop_model_view()

        # disable depth testing
        director.set_depth_test( False )

        # re-apply the original projection matrix
        self.pygly_viewport.pop_view_matrix()
        glMatrixMode(GL_MODELVIEW)

