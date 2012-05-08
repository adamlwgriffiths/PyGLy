import unittest
import math

import numpy
import pyglet

from pygly.input.digital import Digital


class test_digital( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_digital( self ):
        device = Digital( 'keyboard' )

        def handle_event( device, event, value ):
            self.assertEqual(
                device,
                'keyboard',
                "Incorrect device"
                )
            self.assertEqual(
                event,
                'down',
                "Incorrect event"
                )
            self.assertEqual(
                value[ 0 ],
                'd',
                "Incorrect value"
                )
            self.assertEqual(
                value[ 1 ],
                None,
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

        device.dispatch_event( 'down', ('d',None) )

        device.unregister_handler( handle_event )
        self.assertFalse(
            handle_event in device.handlers,
            "Handler still registered"
            )



if __name__ == '__main__':
    unittest.main()

