import unittest
import math

import numpy

from pygly.uv_generators.box_wrap import BoxWrap


class test_box_wrap( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_box_wrap( self ):
        # ignored anyway
        normals = numpy.array([
            [ 0.0, -1.0, 0.0 ], # back = front face
            [ 0.0, -1.0, 0.0 ],
            [ 0.0, -1.0, 0.0 ],
            [ 0.0, -1.0, 0.0 ],
            [ 1.0, 0.0, 0.0 ],
            [ 1.0, 0.0, 0.0 ]
            ])
        
        vertices = numpy.array([
            [ 0.0, 0.0, 0.0 ],
            [ 0.25, 0.0, 0.0 ],
            [ 0.5, 0.0, 0.0 ],
            [ 1.0, 0.0, 0.0 ],
            [ 1.0, 0.5, 0.25 ],
            [ 1.0, 1.0, 0.5 ],
            ])
        
        # planer from x = 0.0 - +1.0
        # and from z = 0.0 to 1.0 
        position = numpy.array([ 0.0, 0.0, 0.0 ])
        forward = numpy.array([ 0.0, 1.0, 0.0 ])
        up = numpy.array([ 0.0, 0.0, 1.0 ])
        
        uv = BoxWrap(
            position = position,
            forward = forward,
            up = up,
            size = (5.0, 5.0, 5.0)
            )
        
        
        #print vertices
        texture_coords = uv.generate_coordinates( vertices, normals )
        
        self.assertEqual(
            texture_coords[ 0 ][ 0 ],
            -1.0,
            "Box wrap coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 0 ][ 1 ],
            0.0,
            "Box wrap coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 1 ][ 0 ],
            0.0,
            "Box wrap coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 1 ][ 1 ],
            1.0,
            "Box wrap coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 2 ][ 0 ],
            0.5,
            "Box wrap coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 2 ][ 1 ],
            0.5,
            "Box wrap coordinates incorrect"
            )


if __name__ == '__main__':
    unittest.main()

