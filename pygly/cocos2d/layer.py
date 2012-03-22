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
        if self.pygly_viewport.camera != None:
            self.pygly_viewport.camera().apply_model_view()

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

        # cocos only sets the view matrix up once
        # so we must store the existing view matrix
        # so we can re-apply it at the end of our render
        # store the current projection matrix
        matrix = [ 0.0 for i in range(16)]
        glMatrix = (GLfloat * 16)(*matrix)
        glGetFloatv( GL_PROJECTION_MATRIX, glMatrix )

        # apply our projection matrix
        self.pygly_viewport.camera().view_matrix.apply_view_matrix( self.pygly_viewport )
        glMatrixMode(GL_MODELVIEW)

        glPushMatrix()
        glLoadIdentity()

        # apply the camera transforms
        self.transform()

        # setup the viewport
        self.pygly_viewport.setup_viewport()
        self.pygly_viewport.render( director.window )
        self.pygly_viewport.tear_down_viewport()

        glPopMatrix()

        # disable depth testing
        director.set_depth_test( False )

        # re-apply the original projection matrix
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        glMultMatrixf( glMatrix )
        glMatrixMode(GL_MODELVIEW)

