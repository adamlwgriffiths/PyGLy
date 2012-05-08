import unittest
import math

import numpy
import pyglet

from pygly.dispatcher import Dispatcher


class test_viewport( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_dispatcher( self ):
        obj = Dispatcher()

        def handler():
            pass

        self.assertFalse(
            handler in obj.handlers,
            "IMPOSSIBRU!"
            )
        obj.register_handler( handler )

        self.assertTrue(
            handler in obj.handlers,
            "Handler not registered"
            )

        obj.unregister_handler( handler )
        self.assertFalse(
            handler in obj.handlers,
            "Handler still registered"
            )


if __name__ == '__main__':
    unittest.main()

