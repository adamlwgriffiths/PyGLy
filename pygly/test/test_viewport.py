import unittest
import math

import numpy
import pyglet

from pygly.viewport import Viewport


class test_viewport( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_viewport_creation( self ):
        window = pyglet.window.Window(
            fullscreen = False,
            width = 1024,
            height = 512
            )
        viewport = Viewport(
            [
                [0, 0],
                [1024, 512]
                ]
            )
        self.assertEqual(
            viewport.x,
            0,
            "Viewport x incorrect"
            )
        self.assertEqual(
            viewport.y,
            0,
            "Viewport y incorrect"
            )
        self.assertEqual(
            viewport.width,
            1024,
            "Viewport width incorrect"
            )
        self.assertEqual(
            viewport.height,
            512,
            "Viewport height incorrect"
            )
        self.assertEqual(
            viewport.aspect_ratio,
            2.0,
            "Viewport aspect ratio incorrect"
            )


if __name__ == '__main__':
    unittest.main()

