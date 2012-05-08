import unittest
import math

import numpy
import pyglet

from pygly.input.analog import Analog


class test_analog( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_analog( self ):
        device = Analog( 'mouse', 'x' )

        def handle_event( device, event, value ):
            self.assertEqual(
                device,
                'mouse',
                "Incorrect device"
                )
            self.assertEqual(
                event,
                'x',
                "Incorrect event"
                )
            self.assertEqual(
                value[ 0 ],
                100,
                "Incorrect value"
                )
            self.assertEqual(
                value[ 1 ],
                5,
                "Incorrect value"
                )

        self.assertFalse(
            handle_event in device.handlers,
            "IMPOSSIBRU!"
            )

        device.register_handler( handle_event )
        self.assertTrue(
            handle_event in device.handlers,
            "Handler not registered"
            )

        device.dispatch_event( (100, 5)  )

        device.unregister_handler( handle_event )
        self.assertFalse(
            handle_event in device.handlers,
            "Handler still registered"
            )


if __name__ == '__main__':
    unittest.main()

