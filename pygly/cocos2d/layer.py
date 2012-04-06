'''
Created on 23/03/2012

@author: adam

TODO: apply layer rotation to the model view
TODO: apply layer scaling to the model view
'''

import numpy
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

        # get the layer's world translation matrix
        matrix = self.get_world_transform()

        # apply the layer's transforms to the viewport
        # this includes position and scale
        # position is the bottom left
        # scale is taken from the anchor_x / anchor_y
        # the position and anchor is in pixels
        # our viewport is 0->1
        # so we must convert from pixels to %

        # convert the bottom left and top right
        # to a vector
        # make them relative to the anchor point
        # bottom left
        bl = numpy.array(
            [
                self.anchor_x - matrix.c,
                self.anchor_y - matrix.g
                ],
            dtype = numpy.float32
            )
        # top right
        tr = numpy.array(
            [
                director.window.width - anchor_x
                director.window.height - anchor_y
                ],
            dtype = numpy.float32
            )

        # scale the vectors by the layer's scale
        # matrix.a = X scale
        # matrix.f = Y scale
        bl *= [ matrix.a, matrix.f ]
        tr *= [ matrix.a, matrix.f ]

        # make the vectors a % value
        bl /= director.window.width
        tr /= director.window.width

        # convert the anchor to a % value
        relative_anchor = (
            self.anchor_x / director.window.width,
            self.anchor_y / director.window.height
            )

        # matrix.c = X pos
        # matrix.g = Y pos
        self.pygly_viewport.dimensions = (
            anchor[ 0 ] + bl[ 0 ],
            anchor[ 1 ] + bl[ 1 ],
            anchor[ 0 ] + tr[ 0 ],
            anchor[ 1 ] + tr[ 1 ]
            )

        # enable depth testing
        director.set_depth_test( True )

        window.render(
            director.window,
            [ self.pygly_viewport ]
            )

