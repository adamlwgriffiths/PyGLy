'''
Created on 23/03/2012

@author: adam

TODO: apply layer rotation to the model view
TODO: replace viewport scaling to instead modify the view matrix
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
        anchor = numpy.array(
            [
                self.anchor_x,
                self.anchor_y
                ],
            dtype = numpy.float32
            )

        # convert the bottom left and top right
        # to a vector
        # bottom left
        bl = numpy.array(
            [
                matrix.c,
                matrix.g
                ],
            dtype = numpy.float32
            )
        # top right
        # assume our size == window size
        tr = numpy.array(
            [
                director.window.width,
                director.window.height
                ],
            dtype = numpy.float32
            )

        # make them relative to the anchor point
        bl -= anchor
        tr -= anchor

        # scale the vectors by the layer's scale
        # matrix.a = X scale
        # matrix.f = Y scale
        bl *= [ matrix.a, matrix.f ]
        tr *= [ matrix.a, matrix.f ]

        # convert the anchor to a % value
        window_size = [
            director.window.width,
            director.window.height
            ]

        # convert back to window co-ordinates
        # instead of being relative to anchor
        bl += anchor
        tr += anchor

        # make the vectors a % value
        bl /= director.window.width
        tr /= director.window.width

        # convert our top right to width / height
        tr -= bl

        # matrix.c = X pos
        # matrix.g = Y pos
        self.pygly_viewport.dimensions = (
            bl[ 0 ],
            bl[ 1 ],
            tr[ 0 ],
            tr[ 1 ]
            )

        # enable depth testing
        director.set_depth_test( True )

        window.render(
            director.window,
            [ self.pygly_viewport ]
            )

