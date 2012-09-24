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

from cocos.layer.base_layers import Layer as Layer
from cocos.director import director
from pyglet.gl import *

import pygly.window


class PyGLyLayer( Layer ):
    """
    Provides a Cocos2D layer which renders a PyGLy scene.
    """

    def __init__(
        self,
        camera = None,
        render_callback = None
        ):
        super( PyGLyLayer, self ).__init__()

        self.pygly_camera = camera
        self.render_callback = render_callback

    def transform( self ):
        """
        Apply the model view transform for the camera
        """
        if self.pygly_camera:
            glMatrixMode( GL_MODELVIEW )
            glLoadMatrix( self.pygly_camera.model_view )

    def draw(self, *args, **kwargs):
        """
        Draws a PyGLy scene as a Cocos2D layer

        This is called by Cocos2D Director.
        """
        print 'layer draw'
        super( PyGLyLayer, self ).draw( *args, **kwargs )

        # render the scene
        if self.render_callback:
            self.render_callback( self, *args, **kwargs )

